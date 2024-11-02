import duckdb
import os
from dotenv import load_dotenv
from tqdm import tqdm
import glob
import time
from sqlalchemy import create_engine, text

start_time = time.time()

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as variáveis do arquivo .env
DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')

# Criar a URL de conexão do banco de dados
postgres_conn = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Conexão com o DuckDB e o PostgreSQL
con = duckdb.connect()

# Instalar e carregar o scanner PostgreSQL no DuckDB
con.execute("""
    INSTALL postgres_scanner;
    LOAD postgres_scanner;
""")

# Conectar ao PostgreSQL usando o comando ATTACH
con.execute(f"""
    ATTACH 'dbname={DB_NAME} user={DB_USER} password={DB_PASS} host={DB_HOST} port={DB_PORT}' AS postgres_db (TYPE POSTGRES, SCHEMA 'public');
""")

# Função para ajustar a sequência automaticamente
def ajustar_sequencia(postgres_table, sequence_name, id_column):
    engine = create_engine(postgres_conn)
    with engine.connect() as connection:
        # Ajustar sequência sem cross-database reference
        max_id = connection.execute(text(f"SELECT MAX({id_column}) FROM {postgres_table}")).scalar()
        if max_id is not None:
            connection.execute(text(f"SELECT setval('{sequence_name}', :new_val)"), {"new_val": max_id + 1})
    engine.dispose()

# Função para criar a tabela se ela não existir
def create_table_if_not_exists(postgres_table, schema):
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS postgres_db.public.{postgres_table} AS 
        SELECT * FROM {schema} LIMIT 0;
    """)

# Função para carregar arquivos Parquet e transferir para PostgreSQL
def load_parquet_to_postgres(parquet_dir, postgres_table, sequence_name, id_column):
    # Listar todos os arquivos Parquet
    parquet_files = glob.glob(os.path.join(parquet_dir, '*.parquet'))
    
    # Mensagem de debug
    print(f"Arquivos Parquet encontrados em {parquet_dir}: {parquet_files}")

    if not parquet_files:
        print(f"Nenhum arquivo Parquet encontrado em {parquet_dir}.")
        return  # Saia se não houver arquivos
    
    # Mostrar a barra de progresso
    for parquet_file in tqdm(parquet_files, desc=f"Carregando {postgres_table}", unit="arquivo"):
        # Carregar os arquivos Parquet no DuckDB
        query = f"CREATE OR REPLACE TEMPORARY VIEW temp_view AS SELECT * FROM read_parquet('{parquet_file}');"
        con.execute(query)
        
        # Criar a tabela no PostgreSQL, se não existir
        create_table_if_not_exists(postgres_table, 'temp_view')
        
        # Inserir os dados diretamente no PostgreSQL
        con.execute(f"""
            INSERT INTO postgres_db.public.{postgres_table}
            SELECT * FROM temp_view;
        """)
    
    print(f"Dados de {parquet_dir} carregados na tabela {postgres_table} no PostgreSQL")
    
    # Ajustar a sequência automaticamente após inserir dados
    ajustar_sequencia(postgres_table, sequence_name, id_column)

# Caminhos para as pastas de arquivos Parquet e configurações de sequência
parquet_config = [
    {"dir": './app/backend/datasets/raw_data/employee/', "table": "employees", "sequence": "employees_employee_id_seq", "id_column": "employee_id"},
    {"dir": './app/backend/datasets/raw_data/product/', "table": "products", "sequence": "products_id_seq", "id_column": "id"},
    {"dir": './app/backend/datasets/raw_data/sales/', "table": "sales", "sequence": "sales_id_seq", "id_column": "id"},
    {"dir": './app/backend/datasets/raw_data/supplier/', "table": "suppliers", "sequence": "suppliers_supplier_id_seq", "id_column": "supplier_id"},
]

# Carregar os arquivos Parquet para PostgreSQL de acordo com os modelos de dados
for config in parquet_config:
    load_parquet_to_postgres(config["dir"], config["table"], config["sequence"], config["id_column"])

# Fechar a conexão
con.close()

elapsed_time = time.time() - start_time
print(f"Tempo decorrido: {elapsed_time:.2f} segundos")

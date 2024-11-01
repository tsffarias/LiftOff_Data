import duckdb
import os
from dotenv import load_dotenv
from tqdm import tqdm
import glob
import time

start_time = time.time()

# Remover variáveis previamente carregadas (se houver)
os.environ.pop('DB_HOST_PROD', None)
os.environ.pop('DB_NAME_PROD', None)
os.environ.pop('DB_USER_PROD', None)
os.environ.pop('DB_PASS_PROD', None)
os.environ.pop('DB_PORT_PROD', None)

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv(override=True)

# Obter as variáveis de ambiente para a conexão PostgreSQL
POSTGRES_HOSTNAME = os.getenv('DB_HOST_PROD')
POSTGRES_DBNAME = os.getenv('DB_NAME_PROD')
POSTGRES_USER = os.getenv('DB_USER_PROD')
POSTGRES_PASSWORD = os.getenv('DB_PASS_PROD')
POSTGRES_PORT = os.getenv('DB_PORT_PROD')

# String de conexão para o PostgreSQL
postgres_conn = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

# Conexão com o DuckDB e o PostgreSQL
con = duckdb.connect()

# Instalar e carregar o scanner PostgreSQL no DuckDB
con.execute("""
    INSTALL postgres_scanner;
    LOAD postgres_scanner;
""")

# Conectar ao PostgreSQL usando o comando ATTACH
con.execute(f"""
    ATTACH 'dbname={POSTGRES_DBNAME} user={POSTGRES_USER} host={POSTGRES_HOSTNAME} port={POSTGRES_PORT} password={POSTGRES_PASSWORD}' AS postgres_db (TYPE POSTGRES, SCHEMA 'public');
""")

# Função para criar a tabela se ela não existir
def create_table_if_not_exists(postgres_table, schema):
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS postgres_db.public.{postgres_table} AS 
        SELECT * FROM {schema} LIMIT 0;
    """)

# Função para carregar arquivos Parquet e transferir para PostgreSQL
def load_parquet_to_postgres(parquet_dir, postgres_table):
    # Listar todos os arquivos Parquet
    parquet_files = glob.glob(os.path.join(parquet_dir, '*.parquet'))
    
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

# Caminho para as pastas de arquivos Parquet
parquet_dir_cadastros = './datasets/raw_data/cadastros/'
parquet_dir_pedidos = './datasets/raw_data/pedidos/'

# Carregar os arquivos de cadastros e pedidos para PostgreSQL
load_parquet_to_postgres(parquet_dir_cadastros, 'raw_cadastros')
load_parquet_to_postgres(parquet_dir_pedidos, 'raw_pedidos')

# Fechar a conexão
con.close()

elapsed_time = time.time() - start_time
print(f"Tempo decorrido: {elapsed_time:.2f} segundos")
import duckdb
import os
from dotenv import load_dotenv
from tqdm import tqdm
import glob
import time
import boto3

start_time = time.time()

# Remover variáveis previamente carregadas (se houver)
os.environ.pop('AWS_ACCESS_KEY_ID', None)
os.environ.pop('AWS_SECRET_ACCESS_KEY', None)
os.environ.pop('AWS_BUCKET_NAME', None)
os.environ.pop('AWS_REGION', None)

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv(override=True)

# Obter as variáveis de ambiente para o S3
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')

# Conexão com o S3 usando boto3
s3_client = boto3.client('s3', 
                         aws_access_key_id=AWS_ACCESS_KEY_ID, 
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                         region_name=AWS_REGION)

# Função para fazer upload dos arquivos Parquet para o S3
def upload_parquet_to_s3(file_path, bucket_name, s3_key):
    try:
        # Upload do arquivo
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Arquivo {file_path} carregado para {bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Erro ao carregar o arquivo {file_path}: {e}")

# Função para carregar arquivos Parquet e transferir para o S3
def load_parquet_to_s3(parquet_dir, s3_prefix):
    # Listar todos os arquivos Parquet
    parquet_files = glob.glob(os.path.join(parquet_dir, '*.parquet'))
    
    # Mostrar a barra de progresso
    for parquet_file in tqdm(parquet_files, desc=f"Carregando {s3_prefix}", unit="arquivo"):
        # Carregar o arquivo Parquet no DuckDB (opcional, caso queira realizar alguma operação)
        con = duckdb.connect()
        query = f"CREATE OR REPLACE TEMPORARY VIEW temp_view AS SELECT * FROM read_parquet('{parquet_file}');"
        con.execute(query)
        
        # Opcional: se quiser manipular os dados, pode fazer aqui
        
        # Definir o caminho (key) no S3 onde o arquivo será salvo
        s3_key = f"{s3_prefix}/{os.path.basename(parquet_file)}"
        
        # Fazer upload do arquivo Parquet para o S3
        upload_parquet_to_s3(parquet_file, AWS_BUCKET_NAME, s3_key)
        
        con.close()
    
    print(f"Dados de {parquet_dir} carregados no S3 com prefixo {s3_prefix}")

# Caminho para as pastas de arquivos Parquet
parquet_dir_cadastros = './datasets/raw_data/cadastros/'
parquet_dir_pedidos = './datasets/raw_data/pedidos/'

# Carregar os arquivos de cadastros e pedidos para o S3
load_parquet_to_s3(parquet_dir_cadastros, 'datasets/bronze/cadastros')
load_parquet_to_s3(parquet_dir_pedidos, 'datasets/bronze/pedidos')

elapsed_time = time.time() - start_time
print(f"Tempo decorrido: {elapsed_time:.2f} segundos")
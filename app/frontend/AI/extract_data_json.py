import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv
from datetime import datetime, date
from decimal import Decimal

# Load environment variables
load_dotenv()

# Obter as variáveis do arquivo .env
DB_PORT = os.getenv('DB_PORT_PROD') or '5432'
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_HOST = os.getenv('DB_HOST_PROD')

# Criar a URL de conexão do banco de dados
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@postgres:{DB_PORT}/{DB_NAME}"

# Cria o motor do banco de dados e a sessão
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Custom serializer for non-serializable types
def custom_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Tipo {type(obj)} não é serializável")

# Function to load data from a table and return as a dictionary list
def carregar_dados(tabela):
    session = SessionLocal()
    try:
        query = text(f"SELECT * FROM {tabela};")
        result = session.execute(query)
        colunas = result.keys()
        dados = [dict(zip(colunas, row)) for row in result.fetchall()]
    finally:
        session.close()
    return dados

# Function to save data into a JSON file
def salvar_em_json(dados, file_path):
    with open(file_path, 'w') as file:
        json.dump(dados, file, indent=4, default=custom_serializer)

# Main execution: read data and save into JSON files
if __name__ == "__main__":
    dados_vendas_por_vendedor = carregar_dados("gold_sales_by_seller")
    salvar_em_json(dados_vendas_por_vendedor, "gold_sales_by_seller.json")
    
    dados_gold_vendas_por_produto = carregar_dados("gold_sales_7_days")
    salvar_em_json(dados_gold_vendas_por_produto, "gold_sales_7_days.json")
    
    print("Dados salvos em 'gold_sales_by_seller.json' e 'gold_sales_7_days.json'.")

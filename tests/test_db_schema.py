import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2

load_dotenv(".env")

# Lê as variáveis de ambiente
POSTGRES_USER = os.getenv('DB_USER_PROD')
POSTGRES_PASSWORD = os.getenv('DB_PASS_PROD')
POSTGRES_HOST = os.getenv('DB_HOST_PROD')
POSTGRES_PORT = os.getenv('DB_PORT_PROD')
POSTGRES_DB = os.getenv('DB_NAME_PROD')

conn = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD)

def test_read_data_and_check_schema_sales():
    df = pd.read_sql('SELECT * FROM sales', con=conn)

    # Verificar se o DataFrame não está vazio
    assert not df.empty, "O DataFrame está vazio."

    # Schema esperado
    expected_dtype = {
        'id': 'int64',
        'email_employee': 'object',
        'email_customer': 'object',
        'first_name': 'object',
        'last_name': 'object',
        'phone_number': 'object',
        'price': 'float64',
        'quantity': 'int64',
        'name_product': 'object',
        'date': 'datetime64[ns, UTC]',
        'created_at': 'datetime64[ns, UTC]'
    }

    # Verificar o schema
    print("Schema do DataFrame:", df.dtypes.to_dict())
    assert df.dtypes.to_dict() == expected_dtype, "O schema do DataFrame não corresponde ao esperado."

def test_read_data_and_check_schema_employees():
    df = pd.read_sql('SELECT * FROM employees', con=conn)

    date_cols = ['hire_date', 'birth_date', 'start_date', 'termination_date', 'created_at']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce', utc=True)

    # Verificar se o DataFrame não está vazio
    assert not df.empty, "O DataFrame está vazio."

    expected_dtype = {
        'employee_id': 'int64',
        'manager_id': 'float64',   
        'first_name': 'object',
        'last_name': 'object',
        'email': 'object',
        'phone_number': 'object',
        'hire_date': 'datetime64[ns, UTC]',
        'department_id': 'int64',
        'job_title': 'object',
        'location': 'object',
        'birth_date': 'datetime64[ns, UTC]',
        'gender': 'object',
        'nationality': 'object',
        'start_date': 'datetime64[ns, UTC]',
        'salary': 'float64',
        'termination_date': 'datetime64[ns, UTC]',
        'created_at': 'datetime64[ns, UTC]'
    }

    # Verificar o schema
    print("Schema do DataFrame:", df.dtypes.to_dict())
    assert df.dtypes.to_dict() == expected_dtype, "O schema do DataFrame não corresponde ao esperado."

def test_read_data_and_check_schema_products():
    # Lê os dados da tabela products
    df = pd.read_sql('SELECT * FROM products', con=conn)

    # Converter a coluna de data/datetime manualmente, caso esteja como string
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', utc=True)

    # Verifica se o DataFrame não está vazio
    assert not df.empty, "O DataFrame está vazio."

    # Define o schema esperado
    expected_dtype = {
        'id': 'int64',
        'name': 'object',
        'description': 'object',
        'price': 'float64',
        'categoria': 'object',
        'email_fornecedor': 'object',
        'created_at': 'datetime64[ns, UTC]'
    }

    print("Schema do DataFrame:", df.dtypes.to_dict())

    # Converte o dtypes atual e esperado em strings para comparação
    actual_schema = {col: str(dtype) for col, dtype in df.dtypes.to_dict().items()}
    expected_schema_str = {col: str(dtype) for col, dtype in expected_dtype.items()}

    assert actual_schema == expected_schema_str, f"O schema do DataFrame não corresponde ao esperado.\nEsperado: {expected_schema_str}\nObtido: {actual_schema}"

def test_read_data_and_check_schema_suppliers():
    # Lê os dados da tabela suppliers
    df = pd.read_sql('SELECT * FROM suppliers', con=conn)

    # Converter a coluna de data/datetime caso esteja como string
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', utc=True)

    # Verifica se o DataFrame não está vazio
    assert not df.empty, "O DataFrame está vazio."

    # Define o schema esperado
    expected_dtype = {
        'supplier_id': 'int64',
        'company_name': 'object',
        'contact_name': 'object',
        'email': 'object',
        'phone_number': 'object',
        'website': 'object',
        'address': 'object',
        'product_categories': 'object',
        'primary_product': 'object',
        'created_at': 'datetime64[ns, UTC]'
    }

    print("Schema do DataFrame:", df.dtypes.to_dict())

    # Converter o dtypes atual e esperado em strings para comparação
    actual_schema = {col: str(dtype) for col, dtype in df.dtypes.to_dict().items()}
    expected_schema_str = {col: str(dtype) for col, dtype in expected_dtype.items()}

    assert actual_schema == expected_schema_str, f"O schema do DataFrame não corresponde ao esperado.\nEsperado: {expected_schema_str}\nObtido: {actual_schema}"
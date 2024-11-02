import pandas as pd
from faker import Faker
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime, timedelta
from enum import Enum
import uuid
import random
import time
import os

# Inicializando o Faker para dados em português
fake = Faker('pt_BR')

class GenderEnum(Enum):
    """
    Enum representando os gêneros dos funcionários.
    """
    male = "Masculino"
    female = "Feminino"
    prefer_not_to_say = "Prefiro não dizer"

class CategoriaBase(Enum):
    """
    Enum representando as categorias de produtos.
    """
    categoria1 = "Eletrônico"
    categoria2 = "Eletrodoméstico"
    categoria3 = "Móveis"
    categoria4 = "Roupas"
    categoria5 = "Calçados"

class ProductCategoriesEnum(str, Enum):
    categoria1 = "Categoria 1"
    categoria2 = "Categoria 2"
    categoria3 = "Categoria 3"

class ProdutoEnum(str, Enum):
    produto1 = "ZapFlow com Gemini"
    produto2 = "ZapFlow com chatGPT"
    produto3 = "ZapFlow com Llama3.0"

# Função para gerar dados de funcionários (employees)
def gerar_dados_employee(n_linhas=5000):
    data = []
    ids_gerados = set()  # Conjunto para rastrear os IDs gerados
    emails_gerados = set()  # Conjunto para rastrear os emails gerados
    
    for _ in range(n_linhas):
        employee_id = len(ids_gerados) + 1  # Garante que o ID seja único e sequencial
        ids_gerados.add(employee_id)  # Adiciona o ID ao conjunto
        
        email = fake.email()
        while email in emails_gerados:  # Gera um novo email se já existir
            email = fake.email()
        emails_gerados.add(email)  # Adiciona o email ao conjunto
        
        data.append({
            'employee_id': employee_id,
            'manager_id': random.choice([None, random.randint(1, 100000)]),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': email,
            'phone_number': fake.phone_number(),
            'hire_date': fake.date_between(start_date='-10y', end_date='today'),
            'department_id': random.randint(1, 20),
            'job_title': fake.job(),
            'location': f"{fake.city()}, {fake.state()}, Brasil",
            'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=70),
            'gender': random.choice(list(GenderEnum)).value,
            'nationality': 'Brasileiro(a)',
            'start_date': fake.date_between(start_date='-5y', end_date='today'),
            'salary': round(random.uniform(2000, 15000), 2),
            'termination_date': fake.date_between(start_date='-2y', end_date='today') if random.random() < 0.1 else None,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
    
    return pd.DataFrame(data)


# Função para gerar dados de produtos (products)
def gerar_dados_product(n_linhas=5000):
    data = []
    ids_gerados = set()  # Conjunto para rastrear os IDs gerados
    emails_gerados = set()  # Conjunto para rastrear os emails gerados

    while len(data) < n_linhas:
        product_id = random.randint(1, 100000)
        while product_id in ids_gerados:  # Gera um novo ID se já existir
            product_id = random.randint(1, 100000)
        ids_gerados.add(product_id)  # Adiciona o ID ao conjunto

        email_fornecedor = fake.email()
        while email_fornecedor in emails_gerados:  # Gera um novo email se já existir
            email_fornecedor = fake.email()
        emails_gerados.add(email_fornecedor)  # Adiciona o email ao conjunto

        data.append({
            'id': product_id,
            'name': fake.word(),
            'description': fake.text(max_nb_chars=100),
            'price': round(random.uniform(10, 5000), 2),
            'categoria': random.choice(list(CategoriaBase)).value,
            'email_fornecedor': email_fornecedor,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
    
    return pd.DataFrame(data)

# Função para gerar dados de vendas (sales)
def gerar_dados_sales(n_linhas=5000):
    data = []
    
    for sale_id in range(1, n_linhas + 1): 
        data.append({
            'id': sale_id,
            'email': fake.email(),
            'valor': round(random.uniform(50, 2000), 2),
            'quantidade': random.randint(1, 10),
            'produto':  random.choice(list(ProdutoEnum)).value,
            'data': fake.date_time_between(start_date='-2y', end_date='now'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
    
    return pd.DataFrame(data)
# Função para gerar dados de fornecedores (suppliers)
def gerar_dados_supplier(n_linhas=5000):
    data = []
    ids_gerados = set()  # Conjunto para rastrear os IDs gerados
    emails_gerados = set()  # Conjunto para rastrear os emails gerados

    while len(data) < n_linhas:
        supplier_id = random.randint(1, 100000)
        while supplier_id in ids_gerados:  # Gera um novo ID se já existir
            supplier_id = random.randint(1, 100000)
        ids_gerados.add(supplier_id)  # Adiciona o ID ao conjunto

        email = fake.email()
        while email in emails_gerados:  # Gera um novo email se já existir
            email = fake.email()
        emails_gerados.add(email)  # Adiciona o email ao conjunto

        data.append({
            'supplier_id': supplier_id,
            'company_name': fake.company(),
            'contact_name': fake.name(),
            'email': email,
            'phone_number': fake.phone_number(),
            'website': fake.url(),
            'address': f"{fake.street_name()}, {fake.building_number()}, {fake.neighborhood()}, {fake.city()}",
            'product_categories': random.choice(list(ProductCategoriesEnum)).value,
            'primary_product': fake.word(),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
    
    return pd.DataFrame(data)


# Definindo caminhos para salvar os dados
caminho_raw_employee = './app/backend/datasets/raw_data/employee/'
caminho_raw_product = './app/backend/datasets/raw_data/product/'
caminho_raw_sales = './app/backend/datasets/raw_data/sales/'
caminho_raw_supplier = './app/backend/datasets/raw_data/supplier/'

# Gerando e salvando os arquivos em Parquet para cada tabela
for func, caminho, nome_tabela in [
        (gerar_dados_employee, caminho_raw_employee, 'employees'),
        (gerar_dados_product, caminho_raw_product, 'products'),
        (gerar_dados_sales, caminho_raw_sales, 'sales'),
        (gerar_dados_supplier, caminho_raw_supplier, 'suppliers')]:

    # Ensure the directory exists
    os.makedirs(caminho, exist_ok=True)

    df = func()  # Gerando os dados
    table = pa.Table.from_pandas(df)  # Convertendo para tabela Parquet
    data_referencia = datetime.today().strftime('%Y-%m-%d')  # Data de referência para nome do arquivo
    arquivo_saida = f'{caminho}{nome_tabela}_{data_referencia}.parquet'
    
    print(f'Escrevendo arquivo em: {arquivo_saida}')  # Adicione esta linha para depuração
    pq.write_table(table, arquivo_saida)
    print(f'Arquivo {nome_tabela} para {data_referencia} gerado com sucesso.')

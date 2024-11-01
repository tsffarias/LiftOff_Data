import pandas as pd
from faker import Faker
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime, timedelta
import uuid
import random
import time

start_time = time.time()
# Inicializando o Faker para geração de dados
fake = Faker('pt_BR')  # Configurando Faker para gerar dados em português

# Função para gerar dados de um "dia" para a tabela de cadastros
def gerar_dados_cadastro(n_linhas=5000):
    data = []
    for _ in range(n_linhas):
        data.append({
            'id': str(uuid.uuid4()),  # Gerando um ID único
            'nome': fake.name(),
            'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=90),
            'cpf': fake.cpf(),  # Gerando CPF
            'cep': fake.postcode(),
            'cidade': fake.city(),
            'estado': fake.state(),
            'pais': 'Brasil',
            'genero': fake.random_element(elements=('M', 'F')),
            'telefone': fake.phone_number(),
            'email': fake.email(),
            'data_cadastro': fake.date_between(start_date='-2y', end_date='today')  # Nova coluna
        })
    return pd.DataFrame(data)

# Função para gerar pedidos relacionados aos cadastros
def gerar_dados_pedidos(cadastros_df, n_pedidos=5000):
    data = []
    
    for _ in range(n_pedidos):
        cpf_cliente = random.choice(cadastros_df['cpf'])
        valor_pedido = round(random.uniform(50, 1000), 2)  # Valor do pedido entre 50 e 1000
        valor_frete = round(random.uniform(5, 100), 2)  # Valor do frete entre 5 e 100
        valor_desconto = random.choice([0, round(random.uniform(5, 100), 2)])  # Pode ou não haver desconto
        cupom = fake.word() if valor_desconto > 0 else None  # Se houver desconto, gera um cupom
        
        # Status do pedido com base nas probabilidades
        status = random.choices(
            ['faturado', 'aguardando pagamento', 'cancelado'], 
            weights=[80, 15, 5], 
            k=1
        )[0]
        
        data.append({
            'id_pedido': str(uuid.uuid4()),  # Gerando um ID único para o pedido
            'cpf': cpf_cliente,
            'valor_pedido': valor_pedido,
            'valor_frete': valor_frete,
            'valor_desconto': valor_desconto,
            'cupom': cupom,
            'endereco_entrega_logradouro': fake.street_name(),
            'endereco_entrega_numero': fake.building_number(),
            'endereco_entrega_bairro': fake.neighborhood(),
            'endereco_entrega_cidade': fake.city(),
            'endereco_entrega_estado': fake.state(),
            'endereco_entrega_pais': 'Brasil',
            'status_pedido': status,
            'data_pedido': fake.date_between(start_date='-2y', end_date='today')  # Nova coluna
        })
    return pd.DataFrame(data)

# Definindo a quantidade de dias e caminho de salvamento
dias = 100  # Exemplo: 10 dias de dados
caminho_raw_cadastros = './datasets/raw_data/cadastros/'
caminho_raw_pedidos = './datasets/raw_data/pedidos/'

# Gerando e salvando os arquivos de cadastros e pedidos
for dia in range(dias):
    data_referencia = (datetime.today() - timedelta(days=dia)).strftime('%Y-%m-%d')
    
    # Gerar cadastros
    df_cadastros = gerar_dados_cadastro()
    
    # Convertendo DataFrame para formato Parquet (cadastros)
    table_cadastros = pa.Table.from_pandas(df_cadastros)
    
    # Nome do arquivo Parquet de cadastros com base no dia
    pq.write_table(table_cadastros, f'{caminho_raw_cadastros}cadastros_{data_referencia}.parquet')
    
    print(f'Arquivo de cadastros para {data_referencia} gerado com sucesso.')
    
    # Gerar pedidos usando os cadastros gerados
    df_pedidos = gerar_dados_pedidos(df_cadastros)
    
    # Convertendo DataFrame para formato Parquet (pedidos)
    table_pedidos = pa.Table.from_pandas(df_pedidos)
    
    # Nome do arquivo Parquet de pedidos com base no dia
    pq.write_table(table_pedidos, f'{caminho_raw_pedidos}pedidos_{data_referencia}.parquet')
    
    print(f'Arquivo de pedidos para {data_referencia} gerado com sucesso.')

elapsed_time = time.time() - start_time
print(f"Tempo decorrido: {elapsed_time:.2f} segundos")
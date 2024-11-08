import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Configure sua chave de API como uma variável de ambiente
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Função para ler o arquivo CSV usando pandas
def read_sales_data(file_path):
    try:
        # Lê o arquivo vendas.csv
        sales_data = pd.read_csv(file_path)
        print("Dados de vendas carregados com sucesso:")
        print(sales_data.head())  # Exibe as primeiras linhas dos dados
        return sales_data
    except FileNotFoundError:
        print("Arquivo não encontrado. Verifique o caminho do arquivo.")
        return None

# Função para enviar uma pergunta ao Groq com os dados em JSON
def ask_groq(question, data_json):
    # Cria o conteúdo da mensagem com a pergunta e os dados em JSON
    content = {
        "question": question,
        "sales_data": data_json
    }
    # Envia a pergunta e os dados ao Groq
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": str(content)}],
        model="llama3-8b-8192"  # Certifique-se de escolher o modelo correto
    )
    # Extraindo o conteúdo da resposta
    return chat_completion.choices[0].message.content

# Caminho para o arquivo vendas.csv
file_path = 'vendas.csv'

# Ler os dados do CSV
sales_data = read_sales_data(file_path)

# Verificar se os dados foram carregados com sucesso
if sales_data is not None:
    # Converter o DataFrame para JSON
    sales_data_json = sales_data.to_json(orient='records')
    
    # Fazendo a pergunta ao Groq com os dados em JSON
    question = "Quanto vendemos no dia 2 de setembro?"
    answer = ask_groq(question, sales_data_json)
    
    # Imprimir a resposta
    print(f"Resposta do Groq: {answer}")
else:
    print("Não foi possível enviar a pergunta ao Groq devido a erro na leitura dos dados.")
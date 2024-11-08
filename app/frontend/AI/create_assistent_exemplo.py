import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração da API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Função para criar o assistente com File Search habilitado
def create_assistant_with_file_search():
    assistant = client.beta.assistants.create(
        name="Assistente Especializado em Vendas",
        instructions="Você é um especialista em análise e insights para equipes de vendas, com foco em maximizar o desempenho de vendas, otimizar estoques e melhorar o relacionamento com fornecedores. Sua expertise abrange a análise de dados de produtos, desempenho de vendedores, produtividade dos funcionários, e gestão de fornecedores. Sempre que receber uma solicitação, responda com um resumo conciso, seguido de insights detalhados e recomendações práticas. Sua linguagem deve ser profissional, direta, e prática. Use gráficos e visualizações sempre que possível para simplificar a compreensão dos dados.",
        model="gpt-4o",
        tools=[{"type": "file_search"}],  # Habilitando o file_search
    )
    print(f"Assistente criado com ID: {assistant}")
    return assistant

# Criar um Vector Store para armazenar arquivos
def create_vector_store():
    vector_store = client.beta.vector_stores.create(name="Vendas Data Store")
    print(f"Vector Store criado com ID: {vector_store.id}")
    return vector_store

# Carregar os arquivos JSON no Vector Store e aguardar o processamento
def upload_files_to_vector_store(vector_store, file_paths):
    file_streams = []
    for file_path in file_paths:
        try:
            with open(file_path, "rb") as file:
                file_streams.append(file)
            print(f"Arquivo {file_path} preparado para upload.")
        except FileNotFoundError:
            print(f"Arquivo {file_path} não encontrado.")

    if file_streams:
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )
        print(f"Status do upload: {file_batch.status}")
        print(f"Contagem de arquivos: {file_batch.file_counts}")
    else:
        print("Nenhum arquivo foi preparado para upload.")

# Atualizar o assistente para usar o Vector Store
def update_assistant_with_vector_store(assistant, vector_store):
    client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    print("Assistente atualizado para usar o Vector Store.")

# Criar o assistente com file_search habilitado
assistant = create_assistant_with_file_search()

# Criar um Vector Store e fazer o upload dos arquivos JSON
vector_store = create_vector_store()
upload_files_to_vector_store(vector_store, ["gold_sales_7_days.json", "gold_sales_by_seller.json"])

# Atualizar o assistente com o Vector Store criado
update_assistant_with_vector_store(assistant, vector_store)

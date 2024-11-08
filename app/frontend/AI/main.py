import streamlit as st
import time
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da API e do ID do Assistente
ASSISTANT_ID = "asst_aEIuoXZHAuFDJctbvBaEc3u0"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Função para enviar a pergunta ao assistente e obter a resposta
def responder_pergunta(pergunta):
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"hoje é dia {datetime.now()} {pergunta}",
            }
        ]
    )
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    
    # Verifica o status da execução até sua conclusão
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(1)

    # Obtém a resposta mais recente do thread
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data
    latest_message = messages[0]
    return latest_message.content[0].text.value.strip()

# Função para mostrar a resposta de forma "streaming"
def mostrar_resposta_streaming(resposta):
    with st.chat_message("assistant"):
        # Placeholder para atualizar o texto progressivamente
        resposta_display = st.empty()
        
        # Remove o "pensando..." e começa a mostrar a resposta gradual
        resposta_temporaria = ""
        for char in resposta:
            resposta_temporaria += char  # Adiciona o próximo caractere
            resposta_display.markdown(resposta_temporaria)  # Atualiza o texto exibido
            time.sleep(0.01)  # Intervalo entre caracteres

# Configurações e título estilizado
st.set_page_config(page_title="Assistente Virtual 🤖💬", page_icon="🤖")
st.title("Assistente Virtual 🤖💬")

# Botão para reiniciar a conversa
if st.button("🔄 Reiniciar Conversa"):
    st.session_state.messages = []

# Inicializar o histórico de mensagens na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de entrada de texto para novas perguntas
pergunta = st.chat_input("Digite sua pergunta:")

if pergunta:
    # Armazenar pergunta do usuário no histórico
    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    # Exibir a mensagem "pensando..." antes de chamar a API
    pensando_display = st.empty()  # Placeholder para "pensando..."
    pensando_display.markdown("Pensando... 🤔")  # Exibe "pensando..."

    # Enviar pergunta para o assistente e obter a resposta
    resposta = responder_pergunta(pergunta)
    
    # Remove o "pensando..." e mostra a resposta em modo "streaming"
    pensando_display.empty()  # Remove "pensando..." antes de mostrar a resposta
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    mostrar_resposta_streaming(resposta)


# Prompt "Assistente Especializado em Vendas"
#Você é um especialista em análise e insights para equipes de vendas, com foco em maximizar o desempenho de vendas, otimizar estoques e melhorar o relacionamento com fornecedores. Sua expertise abrange a análise de dados de produtos, desempenho de vendedores, produtividade dos funcionários, e gestão de fornecedores. 
#Sempre que receber uma solicitação, responda com um resumo conciso, seguido de insights detalhados e recomendações práticas. 
#Sua linguagem deve ser profissional, direta, e prática. 
#Use gráficos e visualizações sempre que possível para simplificar a compreensão dos dados.

# Perguntas de teste:
# Qual é o valor do ticket médio dos produtos?
# Qual é o Top 3 vendedores?
# Qual a média de vendas mensais dos produtos?
# Quantos produtos gemini foram vendidos ontem?
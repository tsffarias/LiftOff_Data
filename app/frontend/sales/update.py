import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time, date
import os
from dotenv import load_dotenv
from utils import show_response_message

# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def update():
    with st.form("update_sale"):
        update_id = st.number_input("ID da Venda", min_value=1, format="%d")
        new_email = st.text_input("Novo Email do Vendedor")
        new_data = st.date_input("Nova Data da compra")
        new_hora = st.time_input("Nova Hora da compra")
        new_valor = st.number_input("Novo Valor da venda", min_value=0.0, format="%.2f")
        new_quantidade = st.number_input("Nova Quantidade de produtos", min_value=1, step=1)
        new_produto = st.selectbox("Novo Produto", options=["ZapFlow com Gemini", "ZapFlow com chatGPT", "ZapFlow com Llama3.0"])

        update_button = st.form_submit_button("Atualizar Venda")

        if update_button:
            update_data = {}
            if new_email:
                update_data["email"] = new_email
            if new_data and new_hora:
                update_data["data"] = datetime.combine(new_data, new_hora).isoformat()
            if new_valor > 0:
                update_data["valor"] = new_valor
            if new_quantidade > 0:
                update_data["quantidade"] = new_quantidade
            if new_produto:
                update_data["produto"] = new_produto

            if update_data:
                response = requests.put(
                    f"{os.getenv('BACKEND_URL')}/sales/{update_id}", json=update_data
                )
                show_response_message(response)
            else:
                st.error("Nenhuma informação fornecida para atualização")
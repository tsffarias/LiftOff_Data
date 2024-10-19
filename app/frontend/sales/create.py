import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time, date
import os
from dotenv import load_dotenv

from utils import show_response_message
# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def create():
    with st.form("new_sale"):
        email = st.text_input("Email do Vendedor")
        data = st.date_input("Data da compra", datetime.now())
        hora = st.time_input("Hora da compra", value=time(9, 0))
        valor = st.number_input("Valor da venda", min_value=0.0, format="%.2f")
        quantidade = st.number_input("Quantidade de produtos", min_value=1, step=1)
        produto = st.selectbox("Produto", options=["ZapFlow com Gemini", "ZapFlow com chatGPT", "ZapFlow com Llama3.0"])
        
        submit_button = st.form_submit_button("Adicionar Venda")

        if submit_button:
            data_hora = datetime.combine(data, hora)
            response = requests.post(
                "http://backend:8000/sales/",
                json={
                    "email": email,
                    "data": data_hora.isoformat(),
                    "valor": valor,
                    "quantidade": quantidade,
                    "produto": produto,
                },
            )
            show_response_message(response)
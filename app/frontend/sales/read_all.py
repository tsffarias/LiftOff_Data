import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time, date
import os
from dotenv import load_dotenv
from utils import show_response_message

# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def read_all():
    if st.button("Exibir Todas as Vendas"):
        response = requests.get(f"{os.getenv('BACKEND_URL')}/sales/")
        if response.status_code == 200:
            sales = response.json()
            # Verifica se o JSON está vazio
            if not sales:
                st.warning("⚠️ Nenhuma Venda encontrada!")
                return
            
            df = pd.DataFrame(sales)
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            show_response_message(response)
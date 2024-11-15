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
    if st.button("Exibir Todos os Produtos"):
        response = requests.get(f"{os.getenv('BACKEND_URL')}/products/")
        if response.status_code == 200:
            product = response.json()
            df = pd.DataFrame(product)

            df = df[list([
                "id",
                "name",
                "description",
                "price",
                "categoria",
                "email_fornecedor",
                "created_at",
            ])]

            # Exibe o DataFrame sem o índice
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            show_response_message(response)
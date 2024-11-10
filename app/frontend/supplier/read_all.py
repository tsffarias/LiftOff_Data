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
    if st.button("Exibir Todos os Fornecedores"):
        response = requests.get(f"{os.getenv('BACKEND_URL')}/suppliers/")
        if response.status_code == 200:
            suppliers = response.json()
            df = pd.DataFrame(suppliers)
            st.dataframe(df, hide_index=True, width=None)
        else:
            show_response_message(response)
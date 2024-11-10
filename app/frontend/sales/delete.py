import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time, date
import os
from dotenv import load_dotenv
from utils import show_response_message
# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


def delete():
    delete_id = st.number_input("ID da Venda para Deletar", min_value=1, format="%d")
    if st.button("Deletar Venda"):
        response = requests.delete(f"{os.getenv('BACKEND_URL')}/sales/{delete_id}")
        show_response_message(response)
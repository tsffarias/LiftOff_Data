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
    with st.form("new_supplier"):
        company_name = st.text_input("Nome da Empresa")
        contact_name = st.text_input("Nome do Contato")
        email = st.text_input("Email")
        phone_number = st.text_input("Número de Telefone")
        website = st.text_input("Website")
        address = st.text_area("Endereço")
        product_categories = st.selectbox(
            "Categorias de produtos ou serviços fornecidos",
            options=["Categoria 1", "Categoria 2", "Categoria 3"]
        )
        primary_product = st.text_input("Descrição do Produto ou Serviço contratado")
        submit_button = st.form_submit_button("Adicionar Fornecedor")

        if submit_button:
            response = requests.post(
                f"{os.getenv('BACKEND_URL')}/suppliers/",
                json={
                    "company_name": company_name,
                    "contact_name": contact_name,
                    "email": email,
                    "phone_number": phone_number,
                    "website": website,
                    "address": address,
                    "product_categories": product_categories,
                    "primary_product": primary_product,
                },
            )
            show_response_message(response)
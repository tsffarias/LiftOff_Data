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
    with st.form("update_supplier"):
        update_id = st.number_input("ID do Fornecedor", min_value=1, format="%d")
        new_company_name = st.text_input("Novo Nome da Empresa")
        new_contact_name = st.text_input("Novo Nome do Contato")
        new_email = st.text_input("Novo Email")
        new_phone_number = st.text_input("Novo Número de Telefone")
        new_website = st.text_input("Novo Website")
        new_address = st.text_area("Novo Endereço")
        new_product_categories = st.selectbox(
            "Categorias de produtos ou serviços fornecidos",
            options=["Categoria 1", "Categoria 2", "Categoria 3"]
        )
        new_primary_product = st.text_input("Nova descrição do Produto ou Serviço contratado")

        update_button = st.form_submit_button("Atualizar Fornecedor")

        if update_button:
            update_data = {}
            if new_company_name:
                update_data["company_name"] = new_company_name
            if new_contact_name:
                update_data["contact_name"] = new_contact_name
            if new_email:
                update_data["email"] = new_email
            if new_phone_number:
                update_data["phone_number"] = new_phone_number
            if new_website:
                update_data["website"] = new_website
            if new_address:
                update_data["address"] = new_address
            if new_product_categories:
                update_data["product_categories"] = new_product_categories
            if new_primary_product:
                update_data["primary_product"] = new_primary_product

            if update_data:
                response = requests.put(
                    f"http://backend:8000/suppliers/{update_id}", json=update_data
                )
                show_response_message(response)
            else:
                st.error("Nenhuma informação fornecida para atualização")
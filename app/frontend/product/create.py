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
    # Buscar a lista de fornecedores
    response_suppliers = requests.get(f"{os.getenv('BACKEND_URL')}/suppliers/")
    if response_suppliers.status_code == 200:
        suppliers = response_suppliers.json()
        # Extrair os emails dos fornecedores
        supplier_emails = [supplier['email'] for supplier in suppliers]
        # Inserir "Selecione o Email do Fornecedor" no início da lista
        supplier_emails.insert(0, "Selecione o Email do Fornecedor")
    else:
        show_response_message(response_suppliers)
        supplier_emails = ["Selecione o Email do Fornecedor"]

    with st.form("new_product"):
        name = st.text_input("Nome do Produto")
        description = st.text_area("Descrição do Produto")
        price = st.number_input("Preço", min_value=0.01, format="%f")
        categoria = st.selectbox(
            "Categoria",
            ["Eletrônico", "Eletrodoméstico", "Móveis", "Roupas", "Calçados"],
        )
        email_fornecedor = st.selectbox("Email do Fornecedor", options=supplier_emails)
        submit_button = st.form_submit_button("Adicionar Produto")

        if submit_button:
            # Verificação antes de enviar o formulário
            if email_fornecedor == "Selecione o Email do Fornecedor":
                st.warning("Por favor, selecione um email válido do fornecedor.")
            else:
                response = requests.post(
                    f"{os.getenv('BACKEND_URL')}/products/",
                    json={
                        "name": name,
                        "description": description,
                        "price": price,
                        "categoria": categoria,
                        "email_fornecedor": email_fornecedor,
                    },
                )
                show_response_message(response)
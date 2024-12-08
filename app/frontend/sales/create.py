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
    # Buscar a lista de funcionários
    response_employees = requests.get(f"{os.getenv('BACKEND_URL')}/employees/")
    if response_employees.status_code == 200:
        employees = response_employees.json()
        # Extrair os emails dos funcionários
        emails = [employee['email'] for employee in employees]
        # Inserir "Selecione o Email" no início da lista
        emails.insert(0, "Selecione o Email")
    else:
        show_response_message(response_employees)
        emails = ["Selecione o Email"]

    # Buscar a lista de produtos
    response_products = requests.get(f"{os.getenv('BACKEND_URL')}/products/")
    if response_products.status_code == 200:
        products = response_products.json()
        # Extrair os nomes dos produtos
        product_names = [product['name'] for product in products]
        # Inserir "Selecione o Produto" no início da lista
        product_names.insert(0, "Selecione o Produto")
    else:
        show_response_message(response_products)
        product_names = ["Selecione o Produto"]

    with st.form("new_sale"):
        email = st.selectbox("Email do Vendedor", options=emails)
        email_customer = st.text_input("Email do Cliente")
        first_name = st.text_input("Primeiro nome do Cliente")
        last_name = st.text_input("Ultimo nome do Cliente")
        phone_number = st.text_input("Número de telefone do Cliente")
        data = st.date_input("Data da compra", datetime.now())
        hora = st.time_input("Hora da compra", value=time(9, 0))
        valor = st.number_input("Valor da venda", min_value=0.0, format="%.2f")
        quantidade = st.number_input("Quantidade de produtos", min_value=1, step=1)
        produto = st.selectbox("Produto", options=product_names)
        
        submit_button = st.form_submit_button("Adicionar Venda")

        if submit_button:
            # Verificações antes de enviar o formulário
            if email == "Selecione o Email":
                st.warning("Por favor, selecione um email válido do vendedor.")
            elif produto == "Selecione o Produto":
                st.warning("Por favor, selecione um produto válido.")
            else:
                data_hora = datetime.combine(data, hora)
                response = requests.post(
                    f"{os.getenv('BACKEND_URL')}/sales/",
                    json={
                        "email_employee": email,
                        "email_customer": email_customer,
                        "first_name": first_name,
                        "last_name": last_name,
                        "phone_number": phone_number,
                        "date": data_hora.isoformat(),
                        "price": valor,
                        "quantity": quantidade,
                        "name_product": produto,
                    },
                )
                show_response_message(response)
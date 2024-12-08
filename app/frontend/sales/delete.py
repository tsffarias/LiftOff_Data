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
    
    # Botão para consultar Venda
    if st.button("Buscar Venda"):
        response = requests.get(f"{os.getenv('BACKEND_URL')}/sales/{delete_id}")
        if response.status_code == 200:
            sales = response.json()
            # Verifica se o JSON está vazio
            if not sales:
                st.warning("⚠️ Nenhuma Venda encontrada!")
                return
            
            df = pd.DataFrame([sales])

            # Seleciona as colunas desejadas
            df = df[
                [
                    "id",
                    "email_employee",
                    "email_customer",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "name_product",
                    "price",
                    "quantity",
                    "date"
                ]
            ]

            # Salvando a venda encontrada no estado da sessão
            st.session_state['df_sales_del'] = df
            st.session_state['id_sales_del'] = delete_id
        else:
            st.warning("Venda não encontrada!")
            st.session_state.pop('df_sales_del', None)

    # Exibe as informações do Produto, se encontrado
    if 'df_sales_del' in st.session_state:    
        st.text_input("Email Funcionario:", value=st.session_state["df_sales_del"].at[0, "email_employee"], disabled=True, key="input_email_employee")
        st.text_input("Email Cliente:", value=st.session_state["df_sales_del"].at[0, "email_customer"], disabled=True, key="input_email_customer")
        st.text_input("Primeiro Nome:", value=st.session_state["df_sales_del"].at[0, "first_name"], disabled=True, key="input_first_name")
        st.text_input("Ultimo Nome:", value=st.session_state["df_sales_del"].at[0, "last_name"], disabled=True, key="input_last_name")
        st.text_input("Número Telefone:", value=st.session_state["df_sales_del"].at[0, "phone_number"], disabled=True, key="input_phone_number")
        st.text_input("Produto:", value=st.session_state["df_sales_del"].at[0, "name_product"], disabled=True, key="input_name_product")
        st.text_input("Valor (R$):", value=st.session_state["df_sales_del"].at[0, "price"], disabled=True, key="input_price")
        st.text_input("Quantidade:", value=st.session_state["df_sales_del"].at[0, "quantity"], disabled=True, key="input_quantity")     
        st.text_input("Data Venda:", value=st.session_state["df_sales_del"].at[0, "date"], disabled=True, key="input_date")
        

        # Botão para deletar Venda
        if st.button("Deletar Venda"):
            response = requests.delete(f"{os.getenv('BACKEND_URL')}/sales/{st.session_state['id_sales_del']}")
            if response.status_code == 200:
                st.success("Venda deletada com sucesso!")
                st.session_state.pop('df_sales_del')
                st.session_state.pop('id_sales_del')
            else:
                st.error("Erro ao deletar a Venda!")
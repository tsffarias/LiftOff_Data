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
            df = pd.DataFrame([sales])

            # Seleciona as colunas desejadas
            df = df[
                [
                    "id",
                    "email",
                    "produto",
                    "valor",
                    "quantidade",
                    "data"
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
        st.text_input("Email:", value=st.session_state["df_sales_del"].at[0, "email"], disabled=True, key="input_email")
        st.text_input("Produto:", value=st.session_state["df_sales_del"].at[0, "produto"], disabled=True, key="input_produto")
        st.text_input("Valor (R$):", value=st.session_state["df_sales_del"].at[0, "valor"], disabled=True, key="input_valor")
        st.text_input("Quantidade:", value=st.session_state["df_sales_del"].at[0, "quantidade"], disabled=True, key="input_quantidade")     
        st.text_input("Data Venda:", value=st.session_state["df_sales_del"].at[0, "data"], disabled=True, key="input_data")
        

        # Botão para deletar Venda
        if st.button("Deletar Venda"):
            response = requests.delete(f"{os.getenv('BACKEND_URL')}/sales/{st.session_state['id_sales_del']}")
            if response.status_code == 200:
                st.success("Venda deletada com sucesso!")
                st.session_state.pop('df_sales_del')
                st.session_state.pop('id_sales_del')
            else:
                st.error("Erro ao deletar a Venda!")
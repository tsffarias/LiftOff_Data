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
    delete_id = st.number_input("ID do Fornecedor para Deletar", min_value=1, format="%d")
    
    # Botão para consultar Fornecedor
    if st.button("Buscar Fornecedor"):
        response = requests.get(f"{os.getenv('BACKEND_URL')}/suppliers/{delete_id}")
        if response.status_code == 200:
            suppliers = response.json()
            # Verifica se o JSON está vazio
            if not suppliers:
                st.warning("⚠️ Nenhum Fornecedor encontrado!")
                return
            
            df = pd.DataFrame([suppliers])
            
            # Seleciona as colunas desejadas
            df = df[
                [
                    "supplier_id",
                    "company_name",
                    "contact_name",
                    "primary_product",
                    "email",
                    "phone_number"
                ]
            ]

            # Salvando o funcionário encontrado no estado da sessão
            st.session_state['df_suppliers_del'] = df
            st.session_state['id_suppliers_del'] = delete_id
        else:
            st.warning("Fornecedor não encontrado!")
            st.session_state.pop('df_suppliers_del', None)
        
    # Exibe as informações do Fornecedor, se encontrado
    if 'df_suppliers_del' in st.session_state:    
        st.text_input("Nome da Empresa:", value=st.session_state["df_suppliers_del"].at[0, "company_name"], disabled=True, key="input_company_name")
        st.text_input("Nome de Contato:", value=st.session_state["df_suppliers_del"].at[0, "contact_name"], disabled=True, key="input_contact_name")
        st.text_input("Produto:", value=st.session_state["df_suppliers_del"].at[0, "primary_product"], disabled=True, key="input_primary_product")
        st.text_input("E-mail:", value=st.session_state["df_suppliers_del"].at[0, "email"], disabled=True, key="input_email")
        st.text_input("Telefone:", value=st.session_state["df_suppliers_del"].at[0, "phone_number"], disabled=True, key="input_phone")     

        # Botão para deletar funcionário
        if st.button("Deletar Fornecedor"):
            response = requests.delete(f"{os.getenv('BACKEND_URL')}/suppliers/{st.session_state['id_suppliers_del']}")
            if response.status_code == 200:
                st.success("Fornecedor deletado com sucesso!")
                st.session_state.pop('df_suppliers_del')
                st.session_state.pop('id_suppliers_del')
            else:
                st.error("Erro ao deletar o Fornecedor!")
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time, date
import os
from dotenv import load_dotenv
from utils import show_response_message

# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def read_supplier():
    options = ["Selecione uma opção:", "ID", "Nome Empresa", "Nome Produto"]
    select_search = st.selectbox("Buscar por:", options=options)

    # Determina o estado do campo de entrada de texto
    input_disabled = select_search == "Selecione uma opção:"

    # Determina a mensagem do text_input
    if input_disabled:
        mensagem = "Selecione uma opção de pesquisa"
    else:
        mensagem = f"Pesquisar Fornecedor por {select_search}:"

    # Entrada de texto para pesquisa
    search_field = st.text_input(mensagem, disabled=input_disabled)

    search_supplier_bt = st.button("Buscar fornecedor", disabled=input_disabled)

    if search_supplier_bt:
        # Filtrando o DataFrame com base na entrada do usuário
        if search_field.strip() == "":
            st.warning("Digite uma valor para ser pesquisado!")
        else:
            if not input_disabled and search_field:
                response = requests.get(f"http://backend:8000/suppliers/")

                if response.status_code == 200:
                    supplier = response.json()
                    df = pd.DataFrame(supplier)
                    
                    if select_search == "Nome Empresa":
                        df_supplier = df[df['company_name'].str.contains(search_field, case=False, na=False)]
                    elif select_search == "Nome Produto":
                        df_supplier = df[df['primary_product'].str.contains(search_field, case=False, na=False)]
                    else:  # Assuming 'ID'
                        df_supplier = df[df['supplier_id'].astype(str).str.contains(search_field, case=False, na=False)]
                                                        
                    if not df_supplier.empty:
                        st.dataframe(df_supplier, hide_index=True, width=None)
                    else:
                        st.warning("Nenhum Fornecedor encontrado!")
                else:
                    show_response_message(response)
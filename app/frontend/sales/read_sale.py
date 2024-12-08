import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time, date
import os
from dotenv import load_dotenv
from utils import show_response_message

# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def read_sale():
    options = ["Selecione uma opção:", "ID", "Email", "Produto", "Data"]
    select_search = st.selectbox("Buscar por:", options=options)

    # Determina o estado do campo de entrada de texto
    input_disabled = select_search == "Selecione uma opção:"

    # Determina a mensagem do text_input
    if input_disabled:
        mensagem = "Selecione uma opção de pesquisa"
    else:
        mensagem = f"Pesquisar Venda por {select_search}:"

    if select_search == 'Data':
        search_field = st.date_input("Selecione a Data da Venda", datetime.now())
    else:
        # Entrada de texto para pesquisa
        search_field = st.text_input(mensagem, disabled=input_disabled)

    search_supplier_bt = st.button("Buscar venda", disabled=input_disabled)

    if search_supplier_bt:
        # Filtrando o DataFrame com base na entrada do usuário
        if isinstance(search_field, str) and search_field.strip() == "":
            st.warning("Digite um valor para ser pesquisado!")
        else:
            if not input_disabled and search_field:
                response = requests.get(f"{os.getenv('BACKEND_URL')}/sales/")

                if response.status_code == 200:
                    sales = response.json()
                    # Verifica se o JSON está vazio
                    if not sales:
                        st.warning("⚠️ Nenhuma Venda encontrada!")
                        return
                    df = pd.DataFrame(sales)
                    
                    if select_search == "Email":
                        df_sales = df[df['email'].str.contains(search_field, case=False, na=False)]
                    elif select_search == "Produto":
                        df_sales = df[df['produto'].str.contains(search_field, case=False, na=False)]
                    elif select_search == "Data":
                        search_field_str = search_field.strftime('%Y-%m-%d')
                        df_sales = df[df['data'].str.contains(search_field_str, case=False, na=False)]
                    else:  # Assuming 'ID'
                        df_sales = df[df['id'].astype(str).str.contains(search_field, case=False, na=False)]
                                                        
                    if not df_sales.empty:
                        st.dataframe(df_sales, hide_index=True, use_container_width=True)
                    else:
                        st.warning("Nenhuma Venda encontrada!")
                else:
                    show_response_message(response)
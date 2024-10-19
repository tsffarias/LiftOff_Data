import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time, date
import os
from dotenv import load_dotenv
from utils import show_response_message
# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def read_product():
            options = ["Selecione uma opção:", "ID", "Nome", "Descrição", "Email Fornecedor"]
            select_search = st.selectbox("Buscar por:", options=options)

            # Determina o estado do campo de entrada de texto
            input_disabled = select_search == "Selecione uma opção:"

            # Determina a mensagem do text_input
            if input_disabled == True:
                mensagem = "Selecione uma opção de pesquisa"
            else:
                mensagem = f"Pesquisar Produto por {select_search}:"

            # Entrada de texto para pesquisa
            search_field = st.text_input(mensagem, disabled=input_disabled)

            search_supplier_bt = st.button("Buscar produto" , disabled=input_disabled)

            if search_supplier_bt:
                # Filtrando o DataFrame com base na entrada do usuário
                if search_field.strip() == "":
                    st.warning("Digite uma valor para ser pesquisado!")
                else:
                    if not input_disabled and search_field:
                        response = requests.get(f"http://backend:8000/products/")

                        if response.status_code == 200:
                            product = response.json()
                            df = pd.DataFrame(product)
                            
                            if select_search == "Nome":
                                df_product = df[df['name'].str.contains(search_field, case=False, na=False)]
                            elif select_search == "Descrição":
                                df_product = df[df['description'].str.contains(search_field, case=False, na=False)]
                            elif select_search == "Email Fornecedor":
                                df_product = df[df['email_fornecedor'].str.contains(search_field, case=False, na=False)]
                            else:  # Assuming 'ID'
                                df_product = df[df['id'].astype(str).str.contains(search_field, case=False, na=False)]
                                
                            if not df_product.empty:
                                st.dataframe(df_product, hide_index=True, width=None)
                            else:
                                st.warning("Nenhum Produto encontrado!")
                        else:
                            show_response_message(response)
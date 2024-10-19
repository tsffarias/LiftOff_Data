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
            delete_id = st.number_input("ID do Produto para Deletar", min_value=1, format="%d")
            
            # Botão para consultar Produto
            if st.button("Buscar Produto"):
                response = requests.get(f"http://backend:8000/products/{delete_id}")
                if response.status_code == 200:
                    product = response.json()
                    df = pd.DataFrame([product])

                    # Seleciona as colunas desejadas
                    df = df[
                        [
                            "id",
                            "name",
                            "description",
                            "categoria",
                            "email_fornecedor",
                            "price"
                        ]
                    ]

                    # Salvando o funcionário encontrado no estado da sessão
                    st.session_state['df_product_del'] = df
                    st.session_state['id_product_del'] = delete_id
                else:
                    st.warning("Produto não encontrado!")
                    st.session_state.pop('df_product_del', None)
            
            # Exibe as informações do Produto, se encontrado
            if 'df_product_del' in st.session_state:    
                st.text_input("Nome:", value=st.session_state["df_product_del"].at[0, "name"], disabled=True, key="input_name")
                st.text_input("Descrição:", value=st.session_state["df_product_del"].at[0, "description"], disabled=True, key="input_description")
                st.text_input("Categoria:", value=st.session_state["df_product_del"].at[0, "categoria"], disabled=True, key="input_categoria")
                st.text_input("Preço:", value=st.session_state["df_product_del"].at[0, "price"], disabled=True, key="input_price")     
                st.text_input("E-mail Fornecedor:", value=st.session_state["df_product_del"].at[0, "email_fornecedor"], disabled=True, key="input_email_fornecedor")
                

                # Botão para deletar Produto
                if st.button("Deletar Produto"):
                    response = requests.delete(f"http://backend:8000/products/{st.session_state['id_product_del']}")
                    if response.status_code == 200:
                        st.success("Produto deletado com sucesso!")
                        st.session_state.pop('df_product_del')
                        st.session_state.pop('id_product_del')
                    else:
                        st.error("Erro ao deletar o Produto!")
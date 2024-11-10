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

    update_id = str(st.number_input("Digite o id do Produto:", min_value=1, format="%d"))

    # Botão para consultar cliente
    search_update_product_bt = st.button("Buscar Produto", key="search_product_update_button")

    if search_update_product_bt:
        df = pd.DataFrame()
        response = requests.get(f"{os.getenv('BACKEND_URL')}/products/{update_id}")
        if response.status_code == 200:
            product = response.json()
            df = pd.DataFrame([product])

            df = df[
                [
                    "id",
                    "name",
                    "description",
                    "price",
                    "categoria",
                    "email_fornecedor"
                ]
            ]

        else:
            st.warning("Produto não encontrado!")

        if not df.empty:
            st.session_state['df_product_upd'] = df
            st.session_state['id_product_upd'] = update_id

    # Verifica se o cliente foi encontrado e exibe as informações
    if 'df_product_upd' in st.session_state:
        with st.form("update_product"):
            col1, col2 = st.columns([2, 3])

            options = ["Eletrônico", "Eletrodoméstico", "Móveis", "Roupas", "Calçados"]
            current_option = st.session_state["df_product_upd"].at[0, "categoria"]
            category_index = options.index(current_option) if current_option in options else 0

            with col1:
                new_name = st.text_input("Novo Nome do Produto", value=st.session_state["df_product_upd"].at[0, "name"], disabled=False, key="input_name_product")
                new_price = st.number_input("Novo Preço", min_value=0.01, format="%.2f", value=st.session_state["df_product_upd"].at[0, "price"], disabled=False, key="input_price_product")
                new_email = st.text_input("Novo Email do Fornecedor", value=st.session_state["df_product_upd"].at[0, "email_fornecedor"], disabled=False, key="input_email_product_supplier")

            with col2:
                new_description = st.text_area("Nova Descrição do Produto", value=st.session_state["df_product_upd"].at[0, "description"], disabled=False, key="input_description_product")
                new_categoria = st.selectbox("Nova Categoria de produtos", options=options, index=category_index, disabled=False, key="input_category_product_form")         
            
            update_product_bt = st.form_submit_button("Atualizar Produto")

            if update_product_bt:
                product_updated = {}
                product_updated["name"] = new_name
                product_updated["price"] = new_price
                product_updated["email_fornecedor"] = new_email
                product_updated["description"] = new_description
                product_updated["categoria"] = new_categoria

                if product_updated:
                    response = requests.put(
                            f"{os.getenv('BACKEND_URL')}/products/{st.session_state['id_product_upd']}", json=product_updated
                        )
                    
                    if response.status_code == 200:
                        st.success("Produto atualizado com sucesso!")
                        del st.session_state['df_product_upd']
                        del st.session_state['id_product_upd']
                    else:
                        st.error("Erro ao atualizar Produto.")
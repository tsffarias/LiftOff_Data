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

    update_id = str(st.number_input("Digite o id do Fornecedor:", min_value=1, format="%d"))

    # Botão para consultar fornecedor
    search_update_supplier_bt = st.button("Buscar Fornecedor", key="search_supplier_update_button")

    if search_update_supplier_bt:
        df = pd.DataFrame()
        response = requests.get(f"{os.getenv('BACKEND_URL')}/suppliers/{update_id}")
        if response.status_code == 200:
            supplier = response.json()
            # Verifica se o JSON está vazio
            if not supplier:
                st.warning("⚠️ Nenhum Fornecedor encontrado!")
                return
            
            df = pd.DataFrame([supplier])

            df = df[
                [
                    "supplier_id",
                    "company_name",
                    "contact_name",
                    "email",
                    "phone_number",
                    "website",
                    "address",
                    "product_categories",
                    "primary_product"
                ]
            ]

        else:
            st.warning("Fornecedor não encontrado!")

        if not df.empty:
            st.session_state['df_supplier_upd'] = df
            st.session_state['id_supplier_upd'] = update_id

    # Verifica se o cliente foi encontrado e exibe as informações
    if 'df_supplier_upd' in st.session_state:
        with st.form("update_supplier"):
            col1, col2 = st.columns([2, 3])

            options = ["Categoria 1", "Categoria 2", "Categoria 3"]
            current_option = st.session_state["df_supplier_upd"].at[0, "product_categories"]
            category_index = options.index(current_option) if current_option in options else 0

            with col1:
                new_company_name = st.text_input("Novo Nome da Empresa", value=st.session_state["df_supplier_upd"].at[0, "company_name"], disabled=False, key="input_company_name")
                new_email = st.text_input("Novo Email", value=st.session_state["df_supplier_upd"].at[0, "email"], disabled=False, key="input_email_supplier")
                new_website = st.text_input("Novo Website", value=st.session_state["df_supplier_upd"].at[0, "website"], disabled=False, key="input_website")
                new_product_categories = st.selectbox("Categorias de produtos ou serviços fornecidos", options=options, index=category_index, disabled=False, key="input_category_products_supplier")

            with col2:
                new_contact_name = st.text_input("Novo Nome do Contato", value=st.session_state["df_supplier_upd"].at[0, "contact_name"], disabled=False, key="input_contact_name")
                new_phone_number = st.text_input("Novo Número de Telefone", value=st.session_state["df_supplier_upd"].at[0, "phone_number"], disabled=False, key="input_phone_number")
                new_address = st.text_area("Novo Endereço", value=st.session_state["df_supplier_upd"].at[0, "address"], disabled=False, key="input_address")
                new_primary_product = st.text_input("Nova descrição do Produto ou Serviço contratado", value=st.session_state["df_supplier_upd"].at[0, "primary_product"], disabled=False, key="input_primary_product")

            update_supplier_bt = st.form_submit_button("Atualizar Fornecedor")

            if update_supplier_bt:
                supplier_updated = {}
                supplier_updated["company_name"] = new_company_name
                supplier_updated["contact_name"] = new_contact_name
                supplier_updated["email"] = new_email
                supplier_updated["phone_number"] = new_phone_number
                supplier_updated["website"] = new_website
                supplier_updated["product_categories"] = new_product_categories
                supplier_updated["address"] = new_address
                supplier_updated["primary_product"] = new_primary_product

                if supplier_updated:
                    response = requests.put(
                            f"{os.getenv('BACKEND_URL')}/suppliers/{st.session_state['id_supplier_upd']}", json=supplier_updated
                        )
                    
                    if response.status_code == 200:
                        st.success("Fornecedor atualizado com sucesso!")
                        del st.session_state['df_supplier_upd']
                        del st.session_state['id_supplier_upd']
                    else:
                        st.error("Erro ao atualizar Fornecedor.")

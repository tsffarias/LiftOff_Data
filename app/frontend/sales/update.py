import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def update():
    update_id = str(st.number_input("Digite o id da Venda:", min_value=1, format="%d"))

    # Botão para consultar venda
    search_update_sale_bt = st.button("Buscar Venda", key="search_sale_update_button")

    if search_update_sale_bt:
        df = pd.DataFrame()
        response = requests.get(f"{os.getenv('BACKEND_URL')}/sales/{update_id}")
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

            df['date'] = pd.to_datetime(df['date'])

        else:
            st.warning("Venda não encontrada!")

        if not df.empty:
            st.session_state['df_sales_upd'] = df
            st.session_state['id_sales_upd'] = update_id

    # Buscar emails dos vendedores
    response_employees = requests.get(f"{os.getenv('BACKEND_URL')}/employees/")
    if response_employees.status_code == 200:
        employees = response_employees.json()
        emails = [employee['email'] for employee in employees]
    else:
        emails = []
        st.warning("Não foi possível buscar os emails dos vendedores.")

    # Buscar nomes dos produtos
    response_products = requests.get(f"{os.getenv('BACKEND_URL')}/products/")
    if response_products.status_code == 200:
        products = response_products.json()
        product_names = [product['name'] for product in products]
    else:
        product_names = []
        st.warning("Não foi possível buscar os nomes dos produtos.")

    # Verifica se a venda foi encontrada e exibe as informações
    if 'df_sales_upd' in st.session_state:
        with st.form("update_sales"):
            col1, col2 = st.columns([2, 3])

            with col1:
                # Garante que o email original da venda esteja na lista de opções
                original_email = st.session_state["df_sales_upd"].at[0, "email_employee"]
                if original_email not in emails:
                    emails.insert(0, original_email)

                new_email = st.selectbox(
                    "Novo Email do Vendedor",
                    options=emails,
                    index=emails.index(original_email)
                )
                new_email_customer = st.text_input("Novo Email do Cliente", value=st.session_state["df_sales_upd"].at[0, "email_customer"], disabled=False, key="input_email_customer")
                phone_number = st.text_input("Novo número de telefone Cliente", value=st.session_state["df_sales_upd"].at[0, "phone_number"], disabled=False, key="input_phone_number_customer")
                new_valor = st.number_input("Novo Valor da venda", min_value=0.01, format="%.2f", value=st.session_state["df_sales_upd"].at[0, "price"], disabled=False, key="input_price_sale")
                new_quantidade = st.number_input("Nova Quantidade de produtos", min_value=1, step=1, value=st.session_state["df_sales_upd"].at[0, "quantity"], disabled=False, key="input_quantidade_sale")

            with col2:
                new_first_name = st.text_input("Novo Primeiro nome do Cliente", value=st.session_state["df_sales_upd"].at[0, "first_name"], disabled=False, key="input_firstname_customer")
                new_last_name = st.text_input("Novo Ultimo nome do Cliente", value=st.session_state["df_sales_upd"].at[0, "last_name"], disabled=False, key="input_lastname_customer")
                # Garante que o produto original da venda esteja na lista de opções
                original_product = st.session_state["df_sales_upd"].at[0, "name_product"]
                if original_product not in product_names:
                    product_names.insert(0, original_product)

                new_product = st.selectbox(
                    "Novo Nome do Produto",
                    options=product_names,
                    index=product_names.index(original_product)
                )
                # Extrai a data e hora da coluna 'data'
                current_data = st.session_state["df_sales_upd"].at[0, "date"].date()
                current_hora = st.session_state["df_sales_upd"].at[0, "date"].time()

                # Preenche os campos com os valores extraídos
                new_data = st.date_input("Nova Data da compra", value=current_data, disabled=False, key="input_sale_date")
                new_hora = st.time_input("Nova Hora da compra", value=current_hora, disabled=False, key="input_sale_hour")
               
            update_sale_bt = st.form_submit_button("Atualizar Venda")

            if update_sale_bt:
                update_sale = {}
                update_sale["email_employee"] = new_email
                update_sale["email_customer"] = new_email_customer
                update_sale["first_name"] = new_first_name
                update_sale["last_name"] = new_last_name
                update_sale["phone_number"] = phone_number
                update_sale["name_product"] = new_product
                update_sale["price"] = new_valor
                update_sale["quantity"] = new_quantidade
                
                if new_data is not None and new_hora is not None:
                    # Combina data e hora
                    combined_datetime = datetime.combine(new_data, new_hora)

                    # Adiciona microsegundos manualmente
                    combined_datetime = combined_datetime.replace(microsecond=datetime.now().microsecond)

                    # Torna o objeto datetime ciente do fuso horário UTC
                    combined_datetime = combined_datetime.replace(tzinfo=timezone.utc)

                    # Converte para ISO 8601 com microsegundos e adiciona 'Z' no final
                    update_sale["date"] = combined_datetime.isoformat(timespec='microseconds').replace('+00:00', 'Z')
                else:
                    update_sale["date"] = None                   

                if update_sale:
                    response = requests.put(
                            f"{os.getenv('BACKEND_URL')}/sales/{st.session_state['id_sales_upd']}", json=update_sale
                        )
                    
                    if response.status_code == 200:
                        st.success("Venda atualizada com sucesso!")
                        del st.session_state['df_sales_upd']
                        del st.session_state['id_sales_upd']
                    else:
                        st.error("Erro ao atualizar Venda.")


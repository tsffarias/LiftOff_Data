import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time, date
import os
from dotenv import load_dotenv

from utils import show_response_message

# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def read_employee():
    options = ["Selecione uma opção:", "ID", "Nome", "Sobrenome", "Email", "Telefone"]
    select_search = st.selectbox("Buscar por:", options=options)

    # Determina o estado do campo de entrada de texto
    input_disabled = select_search == "Selecione uma opção:"

    # Determina a mensagem do text_input
    if input_disabled:
        mensagem = "Selecione uma opção de pesquisa"
    else:
        mensagem = f"Pesquisar funcionário por {select_search}:"

    # Entrada de texto para pesquisa
    search_field = st.text_input(mensagem, disabled=input_disabled)

    search_employee_bt = st.button("Buscar funcionário", disabled=input_disabled, key="search_employee_button")

    if search_employee_bt:
        # Filtrando o DataFrame com base na entrada do usuário
        if search_field.strip() == "":
            st.warning("Digite uma valor para ser pesquisado!")
        else:
            if not input_disabled and search_field:
                response = requests.get(f"{os.getenv('BACKEND_URL')}/employees/")

                if response.status_code == 200:
                    employee = response.json()
                    df = pd.DataFrame(employee)
                    
                    if select_search == "Nome":
                        df_employee = df[df['first_name'].str.contains(search_field, case=False, na=False)]
                    elif select_search == "Sobrenome":
                        df_employee = df[df['last_name'].str.contains(search_field, case=False, na=False)]
                    elif select_search == "Email":
                        df_employee = df[df['email'].str.contains(search_field, case=False, na=False)]
                    elif select_search == "Telefone":
                        df_employee = df[df['phone_number'].str.contains(search_field, case=False, na=False)]
                    else:  # Assuming 'ID'
                        df_employee = df[df['employee_id'].astype(str).str.contains(search_field, case=False, na=False)]
                                                    
                    if not df_employee.empty:
                        st.dataframe(df_employee, hide_index=True, use_container_width=True)
                    else:
                        st.warning("Nenhum Funcionário encontrado!")
                else:
                    show_response_message(response)
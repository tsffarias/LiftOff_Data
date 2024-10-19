import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time, date
import os
from dotenv import load_dotenv

# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def delete():
    delete_id = st.number_input("Pesquisar funcionário por ID:", min_value=1, format="%d")

    # Botão para consultar funcionário
    if st.button("Buscar Funcionário", key="search_employee_delete_button"):
        response = requests.get(f"http://backend:8000/employees/{delete_id}")
        if response.status_code == 200:
            employee = response.json()
            df = pd.DataFrame([employee])

            # Seleciona as colunas desejadas
            df = df[
                [
                    "employee_id",
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number"
                ]
            ]

            # Concatenando Nome e Sobrenome
            df["full_name"] = df["first_name"] + " " + df["last_name"]

            # Salvando o funcionário encontrado no estado da sessão
            st.session_state['df_employee_del'] = df
            st.session_state['id_employee_del'] = delete_id
        else:
            st.warning("Funcionário não encontrado!")
            st.session_state.pop('df_employee_del', None)

    # Exibe as informações do funcionário, se encontrado
    if 'df_employee_del' in st.session_state:    
        st.text_input("Nome:", value=st.session_state["df_employee_del"].at[0, "full_name"], disabled=True, key="input_full_name")
        st.text_input("E-mail:", value=st.session_state["df_employee_del"].at[0, "email"], disabled=True, key="input_email")
        st.text_input("Telefone:", value=st.session_state["df_employee_del"].at[0, "phone_number"], disabled=True, key="input_phone")     

        # Botão para deletar funcionário
        if st.button("Deletar Funcionário"):
            response = requests.delete(f"http://backend:8000/employees/{st.session_state['id_employee_del']}")
            if response.status_code == 200:
                st.success("Funcionário deletado com sucesso!")
                st.session_state.pop('df_employee_del')
                st.session_state.pop('id_employee_del')
            else:
                st.error("Erro ao deletar o funcionário!")


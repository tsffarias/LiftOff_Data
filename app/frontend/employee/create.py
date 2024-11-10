import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time, date
import os
from dotenv import load_dotenv

from utils import show_response_message

# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def create():
    # Adicionar Funcionário
    with st.form("new_employee"):
        first_name = st.text_input("Nome")
        last_name = st.text_input("Sobrenome")
        email = st.text_input("Email")
        phone_number = st.text_input("Número de Telefone")
        hire_date = st.date_input("Data de Contratação")
        department_id = st.number_input("ID do Departamento", min_value=1, step=1)
        manager_id = st.number_input("ID do Gerente", min_value=1, step=1)
        job_title = st.text_input("Cargo")
        location = st.text_input("Localização")
        birth_date = st.date_input("Data de Nascimento")
        gender = st.selectbox("Gênero", ["Masculino", "Feminino", "Prefiro não dizer"])
        nationality = st.text_input("Nacionalidade")
        start_date = st.date_input("Data de Início")
        salary = st.number_input("Salário", min_value=0.01, format="%.2f")
        
        submit_button = st.form_submit_button("Adicionar Funcionário")

        if submit_button:
            response = requests.post(f"{os.getenv('BACKEND_URL')}/employees/", json={
                                    "first_name": first_name,
                                    "last_name": last_name,
                                    "email": email,
                                    "phone_number": phone_number,
                                    "hire_date": hire_date.isoformat(),
                                    "department_id": department_id,
                                    "manager_id": manager_id,
                                    "job_title": job_title,
                                    "location": location,
                                    "birth_date": birth_date.isoformat(),
                                    "gender": gender,
                                    "nationality": nationality,
                                    "start_date": start_date.isoformat(),
                                    "salary": salary
                                }
                            )
            show_response_message(response)
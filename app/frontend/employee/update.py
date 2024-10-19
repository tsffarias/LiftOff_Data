import streamlit as st
import pandas as pd
import requests
from datetime import datetime, time, date
import os
from dotenv import load_dotenv

# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def update():
    update_id = str(st.number_input("Digite o id do Funcionário:", min_value=1, format="%d"))

    # Botão para consultar cliente
    search_update_employee_bt = st.button("Buscar Funcionário", key="search_employee_update_button")

    if search_update_employee_bt:
        df = pd.DataFrame()
        response = requests.get(f"http://backend:8000/employees/{update_id}")
        if response.status_code == 200:
            employee = response.json()
            df = pd.DataFrame([employee])

            df = df[
                [
                    "employee_id",
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "department_id",
                    "manager_id",
                    "job_title",
                    "location",
                    "gender",
                    "birth_date",
                    "nationality",
                    "start_date",
                    "salary",
                    "termination_date",
                    "hire_date",
                    "service_duration"
                ]
            ]

            df['hire_date'] = pd.to_datetime(df['hire_date']).dt.date
            df['birth_date'] = pd.to_datetime(df['birth_date']).dt.date
            df['termination_date'] = pd.to_datetime(df['termination_date']).dt.date
            df['start_date'] = pd.to_datetime(df['start_date']).dt.date

        else:
            st.warning("Funcionário não encontrado!")

        if not df.empty:
            st.session_state['df_employee_upd'] = df
            st.session_state['id_employee_upd'] = update_id

    # Verifica se o cliente foi encontrado e exibe as informações
    if 'df_employee_upd' in st.session_state:
        with st.form("update_employee"):
            col1, col2 = st.columns([2, 3])

            gender_options = ["Masculino", "Feminino", "Prefiro não dizer"]
            current_gender = st.session_state["df_employee_upd"].at[0, "gender"]
            gender_index = gender_options.index(current_gender) if current_gender in gender_options else 0

            termination_date = st.session_state["df_employee_upd"].at[0, "termination_date"]
            if pd.isna(termination_date):  # Check if the date is NaT
                termination_date = None

            with col1:
                new_first_name = st.text_input("Novo Nome", value=st.session_state["df_employee_upd"].at[0, "first_name"], disabled=False, key="input_first_name")
                new_email = st.text_input("Novo Email", value=st.session_state["df_employee_upd"].at[0, "email"], disabled=False, key="input_email_employee")
                new_hire_date = st.date_input("Nova Data de Contratação", value=st.session_state["df_employee_upd"].at[0, "hire_date"], disabled=False, key="input_hire_date")
                new_birth_date = st.date_input("Nova Data de Nascimento", value=st.session_state["df_employee_upd"].at[0, "birth_date"], disabled=False, key="input_birth_date")
                new_department_id = st.number_input("Novo ID do Departamento", min_value=1, step=1, value=st.session_state["df_employee_upd"].at[0, "department_id"], disabled=False, key="input_department_id")
                new_job_title = st.text_input("Novo Cargo", value=st.session_state["df_employee_upd"].at[0, "job_title"], disabled=False, key="input_job_title")
                new_gender = st.selectbox("Novo Gênero", gender_options, index=gender_index, disabled=False, key="input_gender")
                new_nationality = st.text_input("Nova Nacionalidade", value=st.session_state["df_employee_upd"].at[0, "nationality"], disabled=False, key="input_nationality")
            with col2:
                new_last_name = st.text_input("Novo Sobrenome", value=st.session_state["df_employee_upd"].at[0, "last_name"], disabled=False, key="input_last_name")
                new_phone_number = st.text_input("Novo Número de Telefone", value=st.session_state["df_employee_upd"].at[0, "phone_number"], disabled=False, key="input_phone_number")
                new_termination_date = st.date_input("Nova Data de Terminação", value=termination_date, disabled=False, key="input_termination_date")
                new_start_date = st.date_input("Nova Data de Início", value=st.session_state["df_employee_upd"].at[0, "start_date"], disabled=False, key="input_start_date")
                new_manager_id = st.number_input("Novo ID do Gerente", min_value=1, step=1, value=st.session_state["df_employee_upd"].at[0, "manager_id"], disabled=False, key="input_manager_id")
                new_salary = st.number_input("Novo Salário", min_value=0.01, format="%.2f", value=st.session_state["df_employee_upd"].at[0, "salary"], disabled=False, key="input_salary")
                new_location = st.text_input("Nova Localização", value=st.session_state["df_employee_upd"].at[0, "location"], disabled=False, key="input_location")

            update_employee_bt = st.form_submit_button("Atualizar Funcionário")

            if update_employee_bt:
                employee_updated = {}
                employee_updated["first_name"] = new_first_name
                employee_updated["last_name"] = new_last_name
                employee_updated["email"] = new_email
                employee_updated["phone_number"] = new_phone_number
                employee_updated["department_id"] = new_department_id
                employee_updated["job_title"] = new_job_title
                employee_updated["gender"] = new_gender
                employee_updated["nationality"] = new_nationality
                employee_updated["manager_id"] = new_manager_id
                employee_updated["salary"] = new_salary
                employee_updated["location"] = new_location

                if new_termination_date is not None:
                    employee_updated["termination_date"] = new_termination_date.strftime("%Y-%m-%d")  # Convert to string
                else:
                    employee_updated["termination_date"] = None

                if new_hire_date is not None:
                    employee_updated["hire_date"] = new_hire_date.strftime("%Y-%m-%d")
                else:
                    employee_updated["hire_date"] = None

                if new_birth_date is not None:
                    employee_updated["birth_date"] = new_birth_date.strftime("%Y-%m-%d")
                else:
                    employee_updated["birth_date"] = None

                if new_start_date is not None:
                    employee_updated["start_date"] = new_start_date.strftime("%Y-%m-%d")
                else:
                    employee_updated["start_date"] = None

                if employee_updated:
                    response = requests.put(
                            f"http://backend:8000/employees/{st.session_state['id_employee_upd']}", json=employee_updated
                        )
                    
                    if response.status_code == 200:
                        st.success("Funcionário atualizado com sucesso!")
                        del st.session_state['df_employee_upd']
                        del st.session_state['id_employee_upd']
                    else:
                        st.error("Erro ao atualizar Funcionário.")
   # utils.py
import streamlit as st

def show_response_message(response):
       if response.status_code == 200:
           st.success("Operação realizada com sucesso!")
       else:
           try:
               data = response.json()
               if "detail" in data:
                   if isinstance(data["detail"], list):
                       errors = "\n".join([error["msg"] for error in data["detail"]])
                       st.error(f"Erro: {errors}")
                   else:
                       st.error(f"Erro: {data['detail']}")
           except ValueError:
               st.error("Erro desconhecido. Não foi possível decodificar a resposta.")
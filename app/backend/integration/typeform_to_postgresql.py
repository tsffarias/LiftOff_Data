import os
import logging
from dotenv import load_dotenv
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Configura o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_env_variables():
    load_dotenv()
    api_token = os.getenv('TYPEFORM_API_TOKEN')
    form_id = os.getenv('TYPEFORM_FORM_ID')
    db_url = os.getenv('SQLALCHEMY_DATABASE_URL')
    
    if not all([api_token, form_id, db_url]):
        raise EnvironmentError("Variáveis de ambiente necessárias não estão definidas.")
    
    return api_token, form_id, db_url

def fetch_typeform_responses(api_token, form_id):
    url = f'https://api.typeform.com/forms/{form_id}/responses'
    headers = {'Authorization': f'Bearer {api_token}'}
    params = {'page_size': 100}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()['items']
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao obter as respostas: {e}")
        return []

def format_responses(responses):
    formatted_responses = []
    for resp in responses:
        formatted_resp = {
            'submitted_at': resp['submitted_at'],
            'response_id': resp['response_id']
        }
        for answer in resp['answers']:
            question_id = answer['field']['id']
            question_type = answer['type']
            if question_type in ['text', 'number', 'date']:
                formatted_resp[question_id] = answer[question_type]
            elif question_type == 'choice':
                formatted_resp[question_id] = answer['choice']['label']
            elif question_type == 'choices':
                formatted_resp[question_id] = ', '.join([choice['label'] for choice in answer['choices']['labels']])
        formatted_responses.append(formatted_resp)
    return formatted_responses

def save_to_csv(df, filename='typeform_responses.csv'):
    df.to_csv(filename, index=False)
    logging.info(f"As respostas foram salvas em '{filename}'")

def save_to_database(df, db_url):
    try:
        engine = create_engine(db_url)
        df.to_sql('typeform_responses', con=engine, if_exists='replace', index=False)
        logging.info("As respostas foram inseridas no banco de dados PostgreSQL.")
    except SQLAlchemyError as e:
        logging.error(f"Erro ao inserir no banco de dados: {e}")

def main():
    try:
        api_token, form_id, db_url = load_env_variables()
        responses = fetch_typeform_responses(api_token, form_id)
        if responses:
            formatted_responses = format_responses(responses)
            df = pd.DataFrame(formatted_responses)
            save_to_csv(df)
            save_to_database(df, db_url)
    except EnvironmentError as e:
        logging.error(e)

if __name__ == "__main__":
    main()

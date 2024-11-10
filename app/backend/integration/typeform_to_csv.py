import os
from dotenv import load_dotenv
import requests
import pandas as pd

def load_environment_variables():
    """Carrega as variáveis de ambiente do arquivo .env"""
    load_dotenv()
    api_token = os.getenv('TYPEFORM_API_TOKEN')
    form_id = os.getenv('TYPEFORM_FORM_ID')
    return api_token, form_id

def fetch_typeform_responses(api_token, form_id):
    """Faz a requisição à API do Typeform e retorna as respostas"""
    url = f'https://api.typeform.com/forms/{form_id}/responses'
    headers = {'Authorization': f'Bearer {api_token}'}
    params = {'page_size': 100}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()['items']
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter as respostas: {e}")
        return None

def format_responses(responses):
    """Formata as respostas obtidas da API"""
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
                formatted_resp[question_id] = ', '.join(answer['choices']['labels'])
        
        formatted_responses.append(formatted_resp)
    return formatted_responses

def save_responses_to_csv(formatted_responses, filename='typeform_responses.csv'):
    """Salva as respostas formatadas em um arquivo CSV"""
    df = pd.DataFrame(formatted_responses)
    df.to_csv(filename, index=False)
    print(f"As respostas foram salvas em '{filename}'")

def main():
    api_token, form_id = load_environment_variables()
    responses = fetch_typeform_responses(api_token, form_id)
    if responses:
        formatted_responses = format_responses(responses)
        save_responses_to_csv(formatted_responses)

if __name__ == "__main__":
    main()

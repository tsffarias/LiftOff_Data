import os
import pandas as pd
from sqlalchemy import create_engine
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def baixar_dados_analytics():
    """Baixa dados do Google Analytics 4 e salva em um banco de dados SQL."""
    client = BetaAnalyticsDataClient()

    property_id = os.getenv("GA_PROPERTY_ID")
    start_date = os.getenv("GA_START_DATE")

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="date"),
            Dimension(name="city"),
            Dimension(name="country"),
            Dimension(name="deviceCategory"),
            Dimension(name="sessionSource"),
            Dimension(name="sessionMedium"),
        ],
        metrics=[
            Metric(name="totalUsers"),
            Metric(name="newUsers"),
            Metric(name="activeUsers"),
            Metric(name="sessions"),
            Metric(name="engagedSessions"),
            Metric(name="averageSessionDuration"),
            Metric(name="screenPageViews"),
            Metric(name="conversions"),
            Metric(name="totalRevenue"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date="today")],
    )
    response = client.run_report(request)

    # Criar listas para armazenar os dados
    data = []
    header = [dim.name for dim in request.dimensions] + [metric.name for metric in request.metrics]

    # Preencher a lista de dados
    for row in response.rows:
        row_data = [dim_value.value for dim_value in row.dimension_values] + [metric_value.value for metric_value in row.metric_values]
        data.append(row_data)

    # Criar um DataFrame com os dados
    df = pd.DataFrame(data, columns=header)

    # Configuração da conexão com o banco de dados PostgreSQL
    # Obter as variáveis do arquivo .env
    DB_PORT = os.getenv('DB_PORT_PROD')
    DB_NAME = os.getenv('DB_NAME_PROD')
    DB_USER = os.getenv('DB_USER_PROD')
    DB_PASS = os.getenv('DB_PASS_PROD')

    # Criar a URL de conexão do banco de dados
    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@postgres:{DB_PORT}/{DB_NAME}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    # Salvar o DataFrame na tabela 'google_analytics_data' do banco de dados
    df.to_sql(name='google_analytics_data', con=engine, if_exists='replace', index=False)

    print("Dados do Google Analytics salvos no banco de dados PostgreSQL.")

if __name__ == "__main__":
    baixar_dados_analytics()
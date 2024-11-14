import streamlit as st
import requests
import duckdb
import os
import pandas as pd
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Carrega o arquivo .env usando um caminho relativo
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Função para exibir uma mensagem em caso de erro
def show_response_message(response):
    st.error(f"Erro {response.status_code}: {response.json().get('detail', 'Erro desconhecido')}")

# Função para fazer requisições assíncronas e retornar dados JSON
def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        show_response_message(response)
        return None

# Função para registrar e exibir dados JSON diretamente no DuckDB
def show_table_from_data(data, table_name):
    if data:
        df_data = pd.DataFrame(data)
        if not df_data.empty:
            conn.register(table_name, df_data)
            result = conn.execute(f"SELECT * FROM {table_name}").fetchdf()
            st.dataframe(result, hide_index=True)
        else:
            st.warning(f"A tabela '{table_name}' está vazia.")
    else:
        st.warning(f"Sem dados disponíveis para '{table_name}'.")

# Função para exibir métricas
def display_metrics(sales_df, employee_df):
    # KPIs
    num_produtos = sales_df['produto'].nunique()
    receita_total = sales_df['valor'].sum()
    num_vendas = sales_df['id'].nunique()
    total_itens = sales_df['quantidade'].sum()
    num_funcionarios = employee_df['employee_id'].nunique()

    # CSS para criar estilo de "card"
    st.markdown("""
        <style>
        .metric-container {
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 10px;
            background-color: #f9f9f9;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin-bottom: 20px;
        }
        .metric-container h4 {
            margin-bottom: 5px;
            font-weight: bold;
        }
        .metric-value {
            font-size: 1.5em;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Dividindo os KPIs em colunas
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        with st.container():
            st.markdown("<div class='metric-container'><h4>📦 Produtos</h4><div class='metric-value'>{}</div></div>".format(num_produtos), unsafe_allow_html=True)

    with col2:
        with st.container():
            st.markdown("<div class='metric-container'><h4>💰 Receita</h4><div class='metric-value'>R$ {:,.2f}</div></div>".format(receita_total), unsafe_allow_html=True)

    with col3:
        with st.container():
            st.markdown("<div class='metric-container'><h4>📈 Vendas</h4><div class='metric-value'>{}</div></div>".format(num_vendas), unsafe_allow_html=True)

    with col4:
        with st.container():
            st.markdown("<div class='metric-container'><h4>📊 Itens Vendidos</h4><div class='metric-value'>{}</div></div>".format(total_itens), unsafe_allow_html=True)

    with col5:
        with st.container():
            st.markdown("<div class='metric-container'><h4>👥 Funcionários</h4><div class='metric-value'>{}</div></div>".format(num_funcionarios), unsafe_allow_html=True)


# Função para gerar e exibir gráficos
def display_charts(sales_df, employee_df):
    # As datas já foram convertidas em 'dashboard()'
    # Converter 'birth_date' se necessário
    if 'birth_date' in employee_df.columns:
        employee_df['birth_date'] = pd.to_datetime(employee_df['birth_date'], errors='coerce')

    # Gráfico de Vendas por Data
    if 'data' in sales_df.columns:
        sales_by_date = sales_df.groupby(sales_df['data'].dt.date)['valor'].sum().reset_index()
        fig_sales_date = px.line(sales_by_date, x='data', y='valor', title="Vendas ao Longo do Tempo")
        st.plotly_chart(fig_sales_date)

    # Gráfico de Vendas por Produto
    sales_by_product = sales_df.groupby('produto')['valor'].sum().reset_index()
    fig_sales_product = px.bar(sales_by_product, x='produto', y='valor', title="Vendas por Produto")
    st.plotly_chart(fig_sales_product)

    # Top 10 Melhores Vendedores
    top_vendedores = sales_df.groupby('email')['valor'].sum().nlargest(10).reset_index()
    fig_top_vendedores = px.bar(top_vendedores, x='email', y='valor', title="Top 10 Melhores Vendedores")
    st.plotly_chart(fig_top_vendedores)

    # Card divisório para separar as seções
    st.markdown("""
        <div style="
            border: 1px solid #ddd;
            padding: 20px;
            margin-top: 40px;
            margin-bottom: 20px;
            border-radius: 10px;
            background-color: #f1f3f4;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        ">
            <h2 style="margin: 0; font-size: 1.5em;">👥 Seção de Funcionários</h2>
            <p style="margin: 10px 0 0; color: #555;">Análise dos dados de funcionários</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Conversão de colunas de data para datetime no employee_df
    if 'hire_date' in employee_df.columns:
        employee_df['hire_date'] = pd.to_datetime(employee_df['hire_date'], errors='coerce')
        # Remover fuso horário se existir
        employee_df['hire_date'] = employee_df['hire_date'].dt.tz_localize(None)

        min_date_hire = employee_df['hire_date'].min().to_pydatetime()
        max_date_hire = employee_df['hire_date'].max().to_pydatetime()

        # Seletor de intervalo de datas para funcionários usando slider
        st.header("Filtro de Data para Funcionários")
        date_range_hire = st.slider(
            "Selecione o intervalo de datas para funcionários (data de contratação):",
            min_value=min_date_hire,
            max_value=max_date_hire,
            value=(min_date_hire, max_date_hire),
            format="DD/MM/YYYY",
            key='hire_date_range'
        )

        # Filtrar o DataFrame de funcionários com base no intervalo selecionado
        if date_range_hire:
            start_datetime_hire, end_datetime_hire = date_range_hire
            employee_df = employee_df[(employee_df['hire_date'] >= start_datetime_hire) & (employee_df['hire_date'] <= end_datetime_hire)]
    else:
        st.warning("A coluna 'hire_date' não está presente nos dados de funcionários.")
    
    # Gráfico de Folha Salarial Mensal
    if 'hire_date' in employee_df.columns:
        employee_df['mes'] = employee_df['hire_date'].dt.to_period('M').astype(str)
        folha_mensal = employee_df.groupby('mes')['salary'].sum().reset_index()
        fig_folha_mensal = px.bar(folha_mensal, x='mes', y='salary', title="Folha Salarial Mensal")
        st.plotly_chart(fig_folha_mensal)

    # Gráfico de Percentual de Gênero
    genero_percent = employee_df['gender'].value_counts(normalize=True) * 100
    fig_genero = px.pie(values=genero_percent, names=genero_percent.index, title="Percentual de Funcionários por Gênero")
    st.plotly_chart(fig_genero)

    # Média Salarial por Cargo
    salario_por_cargo = employee_df.groupby('job_title')['salary'].mean().reset_index()
    fig_salario_cargo = px.bar(salario_por_cargo, x='job_title', y='salary', title="Média Salarial por Cargo")
    st.plotly_chart(fig_salario_cargo)

    # Gráfico de Contratações por Mês
    if 'hire_date' in employee_df.columns:
        employee_df['hire_mes'] = employee_df['hire_date'].dt.to_period('M').astype(str)
        contratacoes_mes = employee_df.groupby('hire_mes')['employee_id'].count().reset_index()
        fig_contratacoes = px.line(contratacoes_mes, x='hire_mes', y='employee_id', title="Contratações por Mês")
        st.plotly_chart(fig_contratacoes)

    # Tabela com aniversariantes do mês atual
    if 'birth_date' in employee_df.columns:
        current_month = pd.to_datetime("today").month
        aniversariantes = employee_df[employee_df['birth_date'].dt.month == current_month]
        st.header("Aniversariantes do Mês")
        st.dataframe(aniversariantes[['first_name', 'last_name', 'email', 'birth_date']], use_container_width=True)


# Função principal do dashboard
def dashboard():
    st.title("Dashboard LiftOff")

    # Configuração inicial da conexão DuckDB
    global conn
    conn = duckdb.connect(database=":memory:")

    # URLs das APIs
    api_urls = {
        "sales": f"{os.getenv('BACKEND_URL')}/sales/",
        "employees": f"{os.getenv('BACKEND_URL')}/employees/"
    }

    # Requisições em paralelo para obter dados
    with ThreadPoolExecutor() as executor:
        results = executor.map(fetch_data, api_urls.values())

    # Transformar dados em DataFrames
    sales_data = next(results)
    employee_data = next(results)
    sales_df = pd.DataFrame(sales_data)
    employee_df = pd.DataFrame(employee_data)

    # Conversão de colunas de data para datetime
    if 'data' in sales_df.columns:
        sales_df['data'] = pd.to_datetime(sales_df['data'], errors='coerce')
        # Remover fuso horário das datas
        sales_df['data'] = sales_df['data'].dt.tz_localize(None)

        min_date_sales = sales_df['data'].min().to_pydatetime()
        max_date_sales = sales_df['data'].max().to_pydatetime()

        # Seletor de intervalo de datas para vendas usando slider
        st.header("Filtro de Data para Vendas")
        date_range_sales = st.slider(
            "Selecione o intervalo de datas para vendas:",
            min_value=min_date_sales,
            max_value=max_date_sales,
            value=(min_date_sales, max_date_sales),
            format="DD/MM/YYYY"
        )

        # Filtrar o DataFrame de vendas com base no intervalo selecionado
        if date_range_sales:
            start_datetime_sales, end_datetime_sales = date_range_sales
            sales_df = sales_df[(sales_df['data'] >= start_datetime_sales) & (sales_df['data'] <= end_datetime_sales)]
    else:
        st.warning("A coluna 'data' não está presente nos dados de vendas.")

    # Exibir métricas e gráficos
    display_metrics(sales_df, employee_df)
    display_charts(sales_df, employee_df)

    # Fechar a conexão DuckDB
    conn.close()

# Executa o dashboard
if __name__ == "__main__":
    dashboard()

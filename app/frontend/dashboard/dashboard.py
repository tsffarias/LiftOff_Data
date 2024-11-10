import streamlit as st
import requests
import duckdb
import os
import pandas as pd
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import plotly.express as px
import plotly.graph_objects as go

# USAR PLOTLY NOS GRAFICOS

# colocar filtro de data

# Tabela sales
# numero de produtos distinctos (card) - é o count distinct da coluna produto em sales
# numero de receia total (card) - é a soma de valor em sales
# numero de vendas total (card) - é count distinct do id da tabela de sales
# numero de itens total (card) - é a soma de quantidade
# grafico de vendas (grafico de linha por data)
# vendas por produto (grafico de barras)
# vendas por categoria (grafico de barras)
# top 10 melhores vendedores por sua venda (grafico de barra com Email do Vendedor e valor na tabela sales)
# vendas por segmentação de horario (café da manhã, aumoço, cafe da tarde e jantar)
# vendas por dia da semana

# tabela employee
# numero quantidade de funcionarios (card) - é o count distinct da coluna employee_id da tabela employee)
# grafico mensal da folha salarial dos funcionarios (grafico de barras) - é a soma da coluna salary pelo data mês da tabela employee
# percentual de funcionarios homens e mulheres (grafico de pizza) - é o percentual da quantidade da coluna gender da tabela employee
# média salarial por job_title (grafico de barras) - é a média da coluna salary pelo job_title da tabela employee
# grafico de linhas com a quantidade de usuarios contratados por mês - é usado a coluna hire_date e o employee_id da tabela employee
# tabela com os dados dos funcionarios em que o aniversaril é no mês atual

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
        .metric-container h3 {
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
    # Conversões de colunas para datetime se existirem
    if 'data' in sales_df.columns:
        sales_df['data'] = pd.to_datetime(sales_df['data'], errors='coerce')

    if 'hire_date' in employee_df.columns:
        employee_df['hire_date'] = pd.to_datetime(employee_df['hire_date'], errors='coerce')
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

    # Transformar dados em DataFrames e exibir tabelas de vendas e funcionários
    sales_df = pd.DataFrame(next(results))
    employee_df = pd.DataFrame(next(results))

    # Exibir métricas e gráficos
    display_metrics(sales_df, employee_df)
    display_charts(sales_df, employee_df)

    # Fechar a conexão DuckDB
    conn.close()

# Executa o dashboard
if __name__ == "__main__":
    dashboard()

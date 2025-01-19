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
    # Verifica se a coluna 'produto' está presente
    if 'name_product' in sales_df.columns:
        num_produtos = sales_df['name_product'].nunique()
    else:
        num_produtos = 0
        st.warning("⚠️ Coluna 'name_product' ausente no DataFrame de vendas.")

    # Verifica se a coluna 'valor' está presente
    if 'price' in sales_df.columns:
        receita_total = sales_df['price'].sum()
    else:
        receita_total = 0.0
        st.warning("⚠️ Coluna 'price' ausente no DataFrame de vendas.")

    # Verifica se a coluna 'id' está presente
    if 'id' in sales_df.columns:
        num_vendas = sales_df['id'].nunique()
    else:
        num_vendas = 0
        st.warning("⚠️ Coluna 'id' ausente no DataFrame de vendas.")

    # Verifica se a coluna 'quantidade' está presente
    if 'quantity' in sales_df.columns:
        total_itens = sales_df['quantity'].sum()
    else:
        total_itens = 0
        st.warning("⚠️ Coluna 'quantidade' ausente no DataFrame de vendas.")

    # Verifica se a coluna 'employee_id' está presente no employee_df
    if 'employee_id' in employee_df.columns:
        num_funcionarios = employee_df['employee_id'].nunique()
    else:
        num_funcionarios = 0
        st.warning("⚠️ Coluna 'employee_id' ausente no DataFrame de funcionários.")

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
    if 'birth_date' in employee_df.columns:
        employee_df['birth_date'] = pd.to_datetime(employee_df['birth_date'], errors='coerce')

    if 'hire_date' in employee_df.columns:
        # Garantir que 'hire_date' esteja no formato datetime
        employee_df['hire_date'] = pd.to_datetime(employee_df['hire_date'], errors='coerce')
        # Remover fuso horário se existir
        employee_df['hire_date'] = employee_df['hire_date'].dt.tz_localize(None)

    # Gráfico de Vendas por Data
    if 'date' in sales_df.columns:
        sales_by_date = sales_df.groupby(sales_df['date'].dt.date)['price'].sum().reset_index()
        # Transformar em gráfico de área
        fig_sales_date = px.area(sales_by_date, x='date', y='price')
        # Calcular a média
        media_vendas = sales_by_date['price'].mean()
        # Adicionar linha de média vermelha
        fig_sales_date.add_hline(y=media_vendas, line_dash="dash", line_color="red",
                                 annotation_text=f"Média: R$ {media_vendas:,.2f}", 
                                 annotation_position="top left")
        st.subheader("Vendas ao Longo do Tempo")
        st.write("Este gráfico mostra a evolução das vendas ao longo do tempo, permitindo identificar tendências e sazonalidades.")
        st.plotly_chart(fig_sales_date)
    else:
        st.warning("A coluna 'date' não está presente nos dados de vendas.")

    # Gráfico de Vendas por Produto
    sales_by_product = sales_df.groupby('name_product')['price'].sum().reset_index()
    fig_sales_product = px.bar(sales_by_product, x='name_product', y='price')
    st.subheader("Vendas por Produto")
    st.write("Este gráfico apresenta o total de vendas por produto, destacando quais produtos geraram mais receita.")
    st.plotly_chart(fig_sales_product)

    # Top 10 Melhores Vendedores
    top_vendedores = sales_df.groupby('email_employee')['price'].sum().nlargest(10).reset_index()
    fig_top_vendedores = px.bar(top_vendedores, x='email_employee', y='price')
    st.subheader("Top 10 Melhores Vendedores")
    st.write("Este gráfico mostra os 10 vendedores com maior volume de vendas, reconhecendo a performance individual.")
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
        # Cálculo da folha salarial mensal considerando todos os funcionários
        employee_df['hire_date'] = pd.to_datetime(employee_df['hire_date'], errors='coerce')
        employee_df['termination_date'] = pd.to_datetime(employee_df['termination_date'], errors='coerce')
        # Remover fuso horário se existir
        employee_df['hire_date'] = employee_df['hire_date'].dt.tz_localize(None)
        employee_df['termination_date'] = employee_df['termination_date'].dt.tz_localize(None)
        
        # Remover registros com 'hire_date' nulo
        employee_df = employee_df[employee_df['hire_date'].notnull()]
        
        # Remover duplicatas
        employee_df = employee_df.drop_duplicates(subset='employee_id')
        
        # Converter 'salary' para numérico
        employee_df['salary'] = pd.to_numeric(employee_df['salary'], errors='coerce')
        
        # Remover registros com 'salary' nulo ou negativo
        employee_df = employee_df[employee_df['salary'] > 0]
        
        # Criar DataFrame auxiliar para armazenar os resultados
        folha_mensal_df = pd.DataFrame()
        
        # Gerar o intervalo de meses desde a primeira contratação até o mês atual
        start_month = employee_df['hire_date'].min().to_period('M')
        end_month = pd.Timestamp.today().to_period('M')
        
        # Gerar todos os meses no intervalo
        all_months = pd.period_range(start=start_month, end=end_month, freq='M')
        
        # Lista para armazenar os resultados
        folha_mensal = []
        
        for month in all_months:
            # Definir o início e fim do mês
            start_of_month = month.to_timestamp()
            end_of_month = month.to_timestamp(how='end')
            
            # Filtrar funcionários ativos no mês
            active_employees = employee_df[
                (employee_df['hire_date'] <= end_of_month) &
                ((employee_df['termination_date'].isna()) | (employee_df['termination_date'] >= start_of_month))
            ]
            
            # Somar os salários mensais dos funcionários ativos
            total_salary = active_employees['salary'].sum()
            folha_mensal.append({'mes': str(month), 'salary': total_salary})
        
        folha_mensal_df = pd.DataFrame(folha_mensal)
        
        # Converter 'mes' para datetime para ordenar corretamente
        folha_mensal_df['mes'] = pd.to_datetime(folha_mensal_df['mes'])
        
        # Ordenar por mês
        folha_mensal_df = folha_mensal_df.sort_values('mes')
        
        # Criar o gráfico
        fig_folha_mensal = px.bar(folha_mensal_df, x='mes', y='salary')
        # Calcular a média
        media_folha = folha_mensal_df['salary'].mean()
        # Adicionar linha de média vermelha
        fig_folha_mensal.add_hline(y=media_folha, line_dash="dash", line_color="red",
                                   annotation_text=f"Média: R$ {media_folha:,.2f}",
                                   annotation_position="top left")
        st.subheader("Folha Salarial Mensal")
        st.write("Este gráfico apresenta o total mensal da folha salarial, indicando os custos com pessoal ao longo do tempo.")
        st.plotly_chart(fig_folha_mensal)
    else:
        st.warning("A coluna 'hire_date' não está presente nos dados de funcionários.")

    # Gráfico de Percentual de Funcionários por Gênero
    genero_percent = employee_df['gender'].value_counts(normalize=True) * 100
    fig_genero = px.pie(values=genero_percent, names=genero_percent.index)
    st.subheader("Percentual de Funcionários por Gênero")
    st.write("Este gráfico ilustra a distribuição percentual de funcionários por gênero na empresa.")
    st.plotly_chart(fig_genero)

    # Média Salarial por Cargo
    salario_por_cargo = employee_df.groupby('job_title')['salary'].mean().reset_index()
    fig_salario_cargo = px.bar(salario_por_cargo, x='job_title', y='salary')
    st.subheader("Média Salarial por Cargo")
    st.write("Este gráfico mostra a média salarial para cada cargo, permitindo comparar remunerações entre posições.")
    st.plotly_chart(fig_salario_cargo)

    # Gráfico de Contratações por Mês
    if 'hire_date' in employee_df.columns:
        employee_df['hire_mes'] = employee_df['hire_date'].dt.to_period('M').astype(str)
        contratacoes_mes = employee_df.groupby('hire_mes')['employee_id'].count().reset_index()

        # Converter 'hire_mes' para datetime para ordenar corretamente
        contratacoes_mes['hire_mes'] = pd.to_datetime(contratacoes_mes['hire_mes'])

        # Transformar em gráfico de área
        fig_contratacoes = px.area(contratacoes_mes, x='hire_mes', y='employee_id')
        # Calcular a média
        media_contratacoes = contratacoes_mes['employee_id'].mean()
        # Adicionar linha de média vermelha
        fig_contratacoes.add_hline(y=media_contratacoes, line_dash="dash", line_color="red",
                                   annotation_text=f"Média: {media_contratacoes:.2f}",
                                   annotation_position="top left")
        st.subheader("Contratações por Mês")
        st.write("Este gráfico mostra o número de funcionários contratados a cada mês, indicando o ritmo de crescimento da equipe.")
        st.plotly_chart(fig_contratacoes)
    else:
        st.warning("A coluna 'hire_date' não está presente nos dados de funcionários")

    # Tabela com aniversariantes do mês atual
    if 'birth_date' in employee_df.columns:
        current_month = pd.to_datetime("today").month
        aniversariantes = employee_df[employee_df['birth_date'].dt.month == current_month]
        st.header("Aniversariantes do Mês")
        st.write("Esta tabela lista os funcionários que fazem aniversário no mês atual.")
        st.dataframe(aniversariantes[['first_name', 'last_name', 'email', 'birth_date']], use_container_width=True)
    else:
        st.warning("A coluna 'birth_date' não está presente nos dados de funcionários.")


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
    if 'date' in sales_df.columns:
        sales_df['date'] = pd.to_datetime(sales_df['date'], errors='coerce')
        # Remover fuso horário das datas
        sales_df['date'] = sales_df['date'].dt.tz_localize(None)

        min_date_sales = sales_df['date'].min().to_pydatetime()
        max_date_sales = sales_df['date'].max().to_pydatetime()

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
            sales_df = sales_df[(sales_df['date'] >= start_datetime_sales) & (sales_df['date'] <= end_datetime_sales)]
    else:
        st.warning("A coluna 'date' não está presente nos dados de vendas.")

    # Exibir métricas e gráficos
    display_metrics(sales_df, employee_df)
    display_charts(sales_df, employee_df)

    # Fechar a conexão DuckDB
    conn.close()

# Executa o dashboard
if __name__ == "__main__":
    dashboard()

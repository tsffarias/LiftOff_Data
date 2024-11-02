import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import requests
from datetime import datetime, time, date
from utils import show_response_message

from employee import create as create_employee, delete as delete_employee, read_all as read_all_employee, read_employee, update as update_employee
from product import create as create_product, delete as delete_product, read_all as read_all_product, read_product, update as update_product
from sales import create as create_sale, delete as delete_sale, read_all as read_all_sales, read_sale, update as update_sale
from supplier import create as create_supplier, delete as delete_supplier, read_all as read_all_supplier, read_supplier, update as update_supplier

st.set_page_config(
            page_title="LiftOff",
            layout="wide",
            initial_sidebar_state="expanded"
)

class Dashboard:
    def __init__(self):
        self.layout()

    def layout(self):
        st.markdown("""
        <style>
        .big-font {
            font-size:80px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        #Options Menu
        with st.sidebar:
            selected = option_menu('LiftOff', ["Home", 'Funcionário', 'Fornecedor', 'Produto', 'Vendas', 'Sobre'], 
                icons=['house', 'person-badge', 'truck', 'box', 'graph-up', 'info-circle'], menu_icon='intersect', default_index=0,
                styles={
                        "container": {"background-color": "#fafafa"},
                        "nav-link": {"--hover-color": "#eee"},
                        "nav-link-selected": {"background-color": "#0068C9"},
                    }
                )
            
        # Menu Lateral
        if selected=="Home":
            self.home()
        elif selected=="Funcionário":
            self.employee() 
        elif selected=="Fornecedor":
            self.supplier()     
        elif selected=="Produto":
            self.product()
        elif selected=="Vendas":
            self.sales()
        else:
            self.about() 

    def home(self):
        st.title('📊 LiftOff Data')
        st.subheader('Arquitetura de Pipeline de Dados Inovadora para Startups 🚀')

        st.divider()

        col1, col2 = st.columns([3, 2])
        with col1:
            st.header('Bem-vindo ao LiftOff Data')
            st.markdown(
                """
                Transforme sua startup com nossa solução de pipeline de dados de última geração!

                ### 🎯 Nossa Missão
                Capacitar startups com uma arquitetura de dados robusta, escalável e econômica, 
                permitindo que você se concentre no crescimento do seu negócio.

                ### 🔑 Principais Benefícios
                - **Economia**: Solução de baixo custo ideal para startups
                - **Eficiência**: Processamento e análise rápida de dados de vendas
                - **Escalabilidade**: Cresce com seu negócio
                - **Integração**: Conecta-se facilmente com APIs e CRMs existentes
                - **Colaboração**: Facilita o trabalho entre engenheiros e analistas de dados

                ### 🛠️ Nossa Tecnologia
                - Pipeline em camadas: Bronze, Silver e Gold
                - Kafka para streaming em tempo real
                - Airbyte para ingestão de dados flexível
                - Airflow para orquestração poderosa
                - DBT para transformações de dados confiáveis
                - Plataforma 'Briefer' para análise colaborativa
                """
            )
        with col2:
            st.image("https://www.scrapehero.com/wp/wp-content/uploads/2019/05/price-monitoring.gif", use_column_width=True)
            st.markdown("### 📈 Visualize seu Sucesso")
            st.metric(label="Aumento na Eficiência de Dados", value="300%", delta="50%")
            st.metric(label="Redução de Custos Operacionais", value="40%", delta="-15%")
            st.metric(label="Tempo de Insights", value="5 min", delta="-55 min")

        st.divider()
        st.subheader("Pronto para decolar? 🚀")
        if st.button("Agende uma Demo"):
            st.success("Obrigado pelo seu interesse! Nossa equipe entrará em contato em breve.")
    
    def product(self):
        st.title("Gerenciamento de Produtos")
        
        # Adicionar Produto
        with st.expander("Adicionar um Novo Produto"):
            create_product()
        # Visualizar Produtos
        with st.expander("Visualizar Produtos"):
            read_all_product()

        # Obter Detalhes de um Produto
        with st.expander("Obter Detalhes de um Produto"):
            read_product()
            
        # Deletar Produto
        with st.expander("Deletar Produto"):
            delete_product()

        # Atualizar Produto
        with st.expander("Atualizar Produto"):
            update_product()

    def employee(self): 
        st.title("Gerenciamento de Funcionários")
        
        # Criar funcionário
        with st.expander("Adicionar Novo Funcionário"):
            create_employee()

        # Visualizar Funcionários
        with st.expander("Visualizar Funcionários"):
            read_all_employee()

        # Obter Detalhes de um Funcionário
        with st.expander("Obter Detalhes de um Funcionário"):
            read_employee()

        # Deletar Funcionário
        with st.expander("Deletar Funcionário"):
            delete_employee()
        
        # Atualizar Funcionário
        with st.expander("Atualizar Funcionário"):
            update_employee()

    def supplier(self):
        st.title("Gerenciamento de Fornecedores")

        # Adicionar Fornecedor
        with st.expander("Adicionar um Novo Fornecedor"):
            create_supplier()

        # Visualizar Fornecedores
        with st.expander("Visualizar Fornecedores"):
            read_all_supplier()

        # Obter Detalhes de um Fornecedor
        with st.expander("Obter Detalhes de um Fornecedor"):
            read_supplier()

        # Deletar Fornecedor
        with st.expander("Deletar Fornecedor"):
            delete_supplier()


        # Atualizar Fornecedor
        with st.expander("Atualizar Fornecedor"):
            update_supplier()

    def sales(self):
        st.title("Gerenciamento de Vendas")
        
        # Adicionar Venda
        with st.expander("Adicionar uma Nova Venda"):
            create_sale()

        # Visualizar Vendas
        with st.expander("Visualizar Vendas"):
            read_all_sales()

        # Obter Detalhes de uma Venda
        with st.expander("Obter Detalhes de uma Venda"):
            read_sale()

        # Deletar Venda
        with st.expander("Deletar Venda"):
            delete_sale()

        # Atualizar Venda
        with st.expander("Atualizar Venda"):
            update_sale()
    
    def about(self):
        st.title('Sobre o Projeto LiftOff Data')
        
        st.header('Arquitetura do Projeto')
        st.markdown("""
        Este projeto apresenta uma arquitetura de pipeline de dados inovadora e de baixo custo, projetada especificamente para startups. Nosso foco é na integração eficiente de dados de vendas provenientes de diversas fontes, como APIs e CRMs.

        ### Principais Características:
        - **Escalabilidade:** Solução adaptável ao crescimento da sua startup
        - **Eficiência:** Otimizada para ingestão, transformação e visualização de dados
        - **Colaboração:** Facilita o trabalho conjunto entre engenheiros e analistas de dados

        ### Componentes Chave:
        1. Pipeline em camadas: Bronze, Silver e Gold
        2. Integração com APIs
        3. Kafka para streaming de dados
        4. Airbyte para ingestão de dados
        5. Airflow para orquestração de tarefas
        6. DBT para transformação de dados
        7. Plataforma 'Briefer' para acesso e utilização dos dados transformados
        """)

        st.image("https://raw.githubusercontent.com/tsffarias/LiftOff_Data/refs/heads/main/img/arquitetura_1.3.png", use_column_width=True, caption="Arquitetura do Pipeline de Dados")

        st.divider()

        st.header('Sobre o Criador')
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Thiago Silva Farias
            - 🎓 **Formação:** Sistemas de Informação - UFMS
            - 💼 **Experiência:** Engenheiro de Dados
            - 🔗 **LinkedIn:** [Perfil Profissional](https://www.linkedin.com/in/thiagosilvafarias/)
            - 📁 **GitHub:** [Repositório do Projeto](https://github.com/tsffarias/LiftOff_Data/tree/main)

            Obrigado por visitar o projeto LiftOff Data! Estou sempre aberto para discussões sobre engenharia de dados, arquiteturas de pipeline e tecnologias inovadoras. Não hesite em entrar em contato para trocar ideias ou colaborar em projetos futuros.
            """)

        with col2:
            st.image("https://www.scrapehero.com/wp/wp-content/uploads/2019/05/api-gif.gif", use_column_width=True, caption="Integração de Dados em Ação")

if __name__ == "__main__":
    Dashboard()
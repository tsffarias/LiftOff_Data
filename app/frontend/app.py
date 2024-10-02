import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import requests
import pandas as pd

class Dashboard:
    def __init__(self):
        self.layout()

    def layout(self):
        st.set_page_config(
            page_title="LiftOff",
            layout="wide",
            initial_sidebar_state="expanded")

        st.markdown("""
        <style>
        .big-font {
            font-size:80px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        #Options Menu
        with st.sidebar:
            selected = option_menu('LiftOff', ["Home", 'Produto', 'Sobre'], 
                icons=['house', 'search', 'info-circle'], menu_icon='intersect', default_index=0,
                styles={
                        "container": {"background-color": "#fafafa"},
                        "nav-link": {"--hover-color": "#eee"},
                        "nav-link-selected": {"background-color": "#0068C9"},
                    }
                )
            
        # Menu Lateral
        if selected=="Home":
            self.home()
        elif selected=="Produto":
            self.product()
        else:
            self.about() 

    def home(self):
        st.title('📊 LiftOff Data')
        st.subheader('Arquitetura de Pipeline de Dados para Startups 🚀')

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.header('Introdução')
            st.markdown(
                """
                Este projeto apresenta uma arquitetura de pipeline de dados de baixo custo, projetada para startups que precisam processar e analisar dados de vendas de forma eficiente.

                ## Descrição do Projeto

                Este projeto descreve uma arquitetura de pipeline de dados de baixo custo voltada para startups, com foco em integração de dados de vendas a partir de APIs e CRMs, utilizando tecnologias modernas e acessíveis. O objetivo é criar uma solução escalável para ingestão, transformação e visualização de dados, garantindo que tanto engenheiros de dados quanto analistas possam colaborar eficientemente.

                ## Componentes do Pipeline
                A arquitetura proposta inclui a divisão do pipeline em múltiplas camadas (Bronze, Silver e Gold), integração com APIs, Kafka para streaming, Airbyte para ingestão de dados, Airflow para orquestração e DBT para transformação de dados. A plataforma colaborativa 'Briefer' também é integrada, permitindo que analistas de dados acessem e utilizem os dados transformados de forma eficiente.
                """
            )
        with col2:
             st.image("https://www.scrapehero.com/wp/wp-content/uploads/2019/05/price-monitoring.gif", use_column_width=True)


    # Função auxiliar para exibir mensagens de erro detalhadas
    def show_response_message(self,response):
        if response.status_code == 200:
            st.success("Operação realizada com sucesso!")
        else:
            try:
                data = response.json()
                if "detail" in data:
                    # Se o erro for uma lista, extraia as mensagens de cada erro
                    if isinstance(data["detail"], list):
                        errors = "\n".join([error["msg"] for error in data["detail"]])
                        st.error(f"Erro: {errors}")
                    else:
                        # Caso contrário, mostre a mensagem de erro diretamente
                        st.error(f"Erro: {data['detail']}")
            except ValueError:
                st.error("Erro desconhecido. Não foi possível decodificar a resposta.")
    
    def product(self):
        st.title("Gerenciamento de Produtos")
        
        # Adicionar Produto
        with st.expander("Adicionar um Novo Produto"):
            with st.form("new_product"):
                name = st.text_input("Nome do Produto")
                description = st.text_area("Descrição do Produto")
                price = st.number_input("Preço", min_value=0.01, format="%f")
                categoria = st.selectbox(
                    "Categoria",
                    ["Eletrônico", "Eletrodoméstico", "Móveis", "Roupas", "Calçados"],
                )
                email_fornecedor = st.text_input("Email do Fornecedor")
                submit_button = st.form_submit_button("Adicionar Produto")

                if submit_button:
                    response = requests.post(
                        "http://backend:8000/products/",
                        json={
                            "name": name,
                            "description": description,
                            "price": price,
                            "categoria": categoria,
                            "email_fornecedor": email_fornecedor,
                        },
                    )
                    self.show_response_message(response)
        # Visualizar Produtos
        with st.expander("Visualizar Produtos"):
            if st.button("Exibir Todos os Produtos"):
                response = requests.get("http://backend:8000/products/")
                if response.status_code == 200:
                    product = response.json()
                    df = pd.DataFrame(product)

                    df = df[
                        [
                            "id",
                            "name",
                            "description",
                            "price",
                            "categoria",
                            "email_fornecedor",
                            "created_at",
                        ]
                    ]

                    # Exibe o DataFrame sem o índice
                    st.write(df.to_html(index=False), unsafe_allow_html=True)
                else:
                    self.show_response_message(response)

        # Obter Detalhes de um Produto
        with st.expander("Obter Detalhes de um Produto"):
            get_id = st.number_input("ID do Produto", min_value=1, format="%d")
            if st.button("Buscar Produto"):
                response = requests.get(f"http://backend:8000/products/{get_id}")
                if response.status_code == 200:
                    product = response.json()
                    df = pd.DataFrame([product])

                    df = df[
                        [
                            "id",
                            "name",
                            "description",
                            "price",
                            "categoria",
                            "email_fornecedor",
                            "created_at",
                        ]
                    ]

                    # Exibe o DataFrame sem o índice
                    st.write(df.to_html(index=False), unsafe_allow_html=True)
                else:
                    self.show_response_message(response)

        # Deletar Produto
        with st.expander("Deletar Produto"):
            delete_id = st.number_input("ID do Produto para Deletar", min_value=1, format="%d")
            if st.button("Deletar Produto"):
                response = requests.delete(f"http://backend:8000/products/{delete_id}")
                self.show_response_message(response)

        # Atualizar Produto
        with st.expander("Atualizar Produto"):
            with st.form("update_product"):
                update_id = st.number_input("ID do Produto", min_value=1, format="%d")
                new_name = st.text_input("Novo Nome do Produto")
                new_description = st.text_area("Nova Descrição do Produto")
                new_price = st.number_input(
                    "Novo Preço",
                    min_value=0.01,
                    format="%f",
                )
                new_categoria = st.selectbox(
                    "Nova Categoria",
                    ["Eletrônico", "Eletrodoméstico", "Móveis", "Roupas", "Calçados"],
                )
                new_email = st.text_input("Novo Email do Fornecedor")

                update_button = st.form_submit_button("Atualizar Produto")

                if update_button:
                    update_data = {}
                    if new_name:
                        update_data["name"] = new_name
                    if new_description:
                        update_data["description"] = new_description
                    if new_price > 0:
                        update_data["price"] = new_price
                    if new_email:
                        update_data["email_fornecedor"] = new_email
                    if new_categoria:
                        update_data["categoria"] = new_categoria

                    if update_data:
                        response = requests.put(
                            f"http://backend:8000/products/{update_id}", json=update_data
                        )
                        self.show_response_message(response)
                    else:
                        st.error("Nenhuma informação fornecida para atualização")

    def about(self):
        
        st.title('Arquitetura do Projeto')
        st.write('Este projeto descreve uma arquitetura de pipeline de dados de baixo custo voltada para startups, com foco em integração de dados de vendas a partir de APIs e CRMs, utilizando tecnologias modernas e acessíveis. O objetivo é criar uma solução escalável para ingestão, transformação e visualização de dados, garantindo que tanto engenheiros de dados quanto analistas possam colaborar eficientemente. A arquitetura proposta inclui a divisão do pipeline em múltiplas camadas (Bronze, Silver e Gold), integração com APIs, Kafka para streaming, Airbyte para ingestão de dados, Airflow para orquestração e DBT para transformação de dados. A plataforma colaborativa "Briefer" também é integrada, permitindo que analistas de dados acessem e utilizem os dados transformados de forma eficiente.')

        st.image("https://raw.githubusercontent.com/tsffarias/LiftOff_Data/refs/heads/main/img/arquitetura.png", use_column_width=True)

        st.divider()
        st.title('Criador')
        col1, col2 = st.columns(2)
        with col1:
            st.write('**Nome:** Thiago Silva Farias')
            st.write('**Educação:**  Sistemas de Informações - UFMS')
            st.write('**Experiencia:**  Engenheiro de Dados')
            st.write('**Contato:** [Linkedin](https://www.linkedin.com/in/thiagosilvafarias/)')
            st.write('**Github:** [Projeto](https://github.com/tsffarias/LiftOff_Data/tree/main)')
            st.write('**Obrigado pela visita!**')

        with col2:
            st.image("https://www.scrapehero.com/wp/wp-content/uploads/2019/05/api-gif.gif", use_column_width=True)

        
        
        

if __name__ == "__main__":
    Dashboard()
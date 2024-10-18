import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import requests
from datetime import datetime, time, date

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
                    st.dataframe(df, hide_index=True, width=None)
                else:
                    self.show_response_message(response)

        # Obter Detalhes de um Produto
        with st.expander("Obter Detalhes de um Produto"):
            
            options = ["Selecione uma opção:", "ID", "Nome", "Descrição", "Email Fornecedor"]
            select_search = st.selectbox("Buscar por:", options=options)

            # Determina o estado do campo de entrada de texto
            input_disabled = select_search == "Selecione uma opção:"

            # Determina a mensagem do text_input
            if input_disabled == True:
                mensagem = "Selecione uma opção de pesquisa"
            else:
                mensagem = f"Pesquisar Produto por {select_search}:"

            # Entrada de texto para pesquisa
            search_field = st.text_input(mensagem, disabled=input_disabled)

            search_supplier_bt = st.button("Buscar produto" , disabled=input_disabled)

            if search_supplier_bt:
                # Filtrando o DataFrame com base na entrada do usuário
                if search_field.strip() == "":
                    st.warning("Digite uma valor para ser pesquisado!")
                else:
                    if not input_disabled and search_field:
                        response = requests.get(f"http://backend:8000/products/")

                        if response.status_code == 200:
                            product = response.json()
                            df = pd.DataFrame(product)
                            
                            if select_search == "Nome":
                                df_product = df[df['name'].str.contains(search_field, case=False, na=False)]
                            elif select_search == "Descrição":
                                df_product = df[df['description'].str.contains(search_field, case=False, na=False)]
                            elif select_search == "Email Fornecedor":
                                df_product = df[df['email_fornecedor'].str.contains(search_field, case=False, na=False)]
                            else:  # Assuming 'ID'
                                df_product = df[df['id'].astype(str).str.contains(search_field, case=False, na=False)]
                                
                            if not df_product.empty:
                                st.dataframe(df_product, hide_index=True, width=None)
                            else:
                                st.warning("Nenhum Produto encontrado!")
                        else:
                            self.show_response_message(response)

        # Deletar Produto
        with st.expander("Deletar Produto"):
            delete_id = st.number_input("ID do Produto para Deletar", min_value=1, format="%d")
            
            # Botão para consultar Produto
            if st.button("Buscar Produto"):
                response = requests.get(f"http://backend:8000/products/{delete_id}")
                if response.status_code == 200:
                    product = response.json()
                    df = pd.DataFrame([product])

                    # Seleciona as colunas desejadas
                    df = df[
                        [
                            "id",
                            "name",
                            "description",
                            "categoria",
                            "email_fornecedor",
                            "price"
                        ]
                    ]

                    # Salvando o funcionário encontrado no estado da sessão
                    st.session_state['df_product_del'] = df
                    st.session_state['id_product_del'] = delete_id
                else:
                    st.warning("Produto não encontrado!")
                    st.session_state.pop('df_product_del', None)
            
            # Exibe as informações do Produto, se encontrado
            if 'df_product_del' in st.session_state:    
                st.text_input("Nome:", value=st.session_state["df_product_del"].at[0, "name"], disabled=True, key="input_name")
                st.text_input("Descrição:", value=st.session_state["df_product_del"].at[0, "description"], disabled=True, key="input_description")
                st.text_input("Categoria:", value=st.session_state["df_product_del"].at[0, "categoria"], disabled=True, key="input_categoria")
                st.text_input("Preço:", value=st.session_state["df_product_del"].at[0, "price"], disabled=True, key="input_price")     
                st.text_input("E-mail Fornecedor:", value=st.session_state["df_product_del"].at[0, "email_fornecedor"], disabled=True, key="input_email_fornecedor")
                

                # Botão para deletar Produto
                if st.button("Deletar Produto"):
                    response = requests.delete(f"http://backend:8000/products/{st.session_state['id_product_del']}")
                    if response.status_code == 200:
                        st.success("Produto deletado com sucesso!")
                        st.session_state.pop('df_product_del')
                        st.session_state.pop('id_product_del')
                    else:
                        st.error("Erro ao deletar o Produto!")

            
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

    def employee(self):
        st.title("Gerenciamento de Funcionários")

        # Adicionar Funcionário
        with st.expander("Adicionar um Novo Funcionário"):
            with st.form("new_employee"):
                first_name = st.text_input("Nome")
                last_name = st.text_input("Sobrenome")
                email = st.text_input("Email")
                phone_number = st.text_input("Número de Telefone")
                hire_date = st.date_input("Data de Contratação")
                department_id = st.number_input("ID do Departamento", min_value=1, step=1)
                manager_id = st.number_input("ID do Gerente", min_value=1, step=1)
                job_title = st.text_input("Cargo")
                location = st.text_input("Localização")
                birth_date = st.date_input("Data de Nascimento")
                gender = st.selectbox("Gênero", ["Masculino", "Feminino", "Prefiro não dizer"])
                nationality = st.text_input("Nacionalidade")
                start_date = st.date_input("Data de Início")
                salary = st.number_input("Salário", min_value=0.01, format="%.2f")
                
                submit_button = st.form_submit_button("Adicionar Funcionário")

                if submit_button:
                    response = requests.post(
                        "http://backend:8000/employees/",
                        json={
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "phone_number": phone_number,
                            "hire_date": hire_date.isoformat(),
                            "department_id": department_id,
                            "manager_id": manager_id,
                            "job_title": job_title,
                            "location": location,
                            "birth_date": birth_date.isoformat(),
                            "gender": gender,
                            "nationality": nationality,
                            "start_date": start_date.isoformat(),
                            "salary": salary
                        },
                    )
                    self.show_response_message(response)

        # Visualizar Funcionários
        with st.expander("Visualizar Funcionários"):
            if st.button("Exibir Todos os Funcionários"):
                response = requests.get("http://backend:8000/employees/")
                if response.status_code == 200:
                    employees = response.json()
                    df = pd.DataFrame(employees)
                    st.dataframe(df, hide_index=True, width=None)
                else:
                    self.show_response_message(response)

        # Obter Detalhes de um Funcionário
        with st.expander("Obter Detalhes de um Funcionário"):
            options = ["Selecione uma opção:", "ID", "Nome", "Sobrenome", "Email", "Telefone"]
            select_search = st.selectbox("Buscar por:", options=options)

            # Determina o estado do campo de entrada de texto
            input_disabled = select_search == "Selecione uma opção:"

            # Determina a mensagem do text_input
            if input_disabled == True:
                mensagem = "Selecione uma opção de pesquisa"
            else:
                mensagem = f"Pesquisar funcionário por {select_search}:"

            # Entrada de texto para pesquisa
            search_field = st.text_input(mensagem, disabled=input_disabled)

            search_employee_bt = st.button("Buscar funcionário" , disabled=input_disabled, key="search_employee_button")

            if search_employee_bt:
                # Filtrando o DataFrame com base na entrada do usuário
                if search_field.strip() == "":
                    st.warning("Digite uma valor para ser pesquisado!")
                else:
                    if not input_disabled and search_field:
                        response = requests.get(f"http://backend:8000/employees/")

                        if response.status_code == 200:
                            employee = response.json()
                            df = pd.DataFrame(employee)
                            
                            if select_search == "Nome":
                                df_employee = df[df['first_name'].str.contains(search_field, case=False, na=False)]
                            elif select_search == "Sobrenome":
                                df_employee = df[df['last_name'].str.contains(search_field, case=False, na=False)]
                            elif select_search == "Email":
                                df_employee = df[df['email'].str.contains(search_field, case=False, na=False)]
                            elif select_search == "Telefone":
                                df_employee = df[df['phone_number'].str.contains(search_field, case=False, na=False)]
                            else:  # Assuming 'ID'
                                df_employee = df[df['employee_id'].astype(str).str.contains(search_field, case=False, na=False)]
                                
                            if not df_employee.empty:
                                st.dataframe(df_employee, hide_index=True, width=None)
                            else:
                                st.warning("Nenhum Funcionário encontrado!")
                        else:
                            self.show_response_message(response)


        # Deletar Funcionário
        with st.expander("Deletar Funcionário"):

            delete_id = st.number_input("Pesquisar funcionário por ID:", min_value=1, format="%d")

            # Botão para consultar funcionário
            if st.button("Buscar Funcionário", key="search_employee_delete_button"):
                response = requests.get(f"http://backend:8000/employees/{delete_id}")
                if response.status_code == 200:
                    employee = response.json()
                    df = pd.DataFrame([employee])

                    # Seleciona as colunas desejadas
                    df = df[
                        [
                            "employee_id",
                            "first_name",
                            "last_name",
                            "email",
                            "phone_number"
                        ]
                    ]

                    # Concatenando Nome e Sobrenome
                    df["full_name"] = df["first_name"] + " " + df["last_name"]

                    # Salvando o funcionário encontrado no estado da sessão
                    st.session_state['df_employee_del'] = df
                    st.session_state['id_employee_del'] = delete_id
                else:
                    st.warning("Funcionário não encontrado!")
                    st.session_state.pop('df_employee_del', None)

            # Exibe as informações do funcionário, se encontrado
            if 'df_employee_del' in st.session_state:    
                st.text_input("Nome:", value=st.session_state["df_employee_del"].at[0, "full_name"], disabled=True, key="input_full_name")
                st.text_input("E-mail:", value=st.session_state["df_employee_del"].at[0, "email"], disabled=True, key="input_email")
                st.text_input("Telefone:", value=st.session_state["df_employee_del"].at[0, "phone_number"], disabled=True, key="input_phone")     

                # Botão para deletar funcionário
                if st.button("Deletar Funcionário"):
                    response = requests.delete(f"http://backend:8000/employees/{st.session_state['id_employee_del']}")
                    if response.status_code == 200:
                        st.success("Funcionário deletado com sucesso!")
                        st.session_state.pop('df_employee_del')
                        st.session_state.pop('id_employee_del')
                    else:
                        st.error("Erro ao deletar o funcionário!")


        # Atualizar Funcionário
        with st.expander("Atualizar Funcionário"):

            update_id = str(st.number_input("Digite o id do Funcionário:",min_value=1, format="%d"))

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
                    col1,col2=st.columns([2,3])

                    gender_options = ["Masculino", "Feminino", "Prefiro não dizer"]
                    current_gender = st.session_state["df_employee_upd"].at[0, "gender"]
                    gender_index = gender_options.index(current_gender) if current_gender in gender_options else 0

                    termination_date = st.session_state["df_employee_upd"].at[0, "termination_date"]
                    if pd.isna(termination_date):  # Check if the date is NaT
                        termination_date = None

                    with col1:
                        new_first_name = st.text_input("Novo Nome", value=st.session_state["df_employee_upd"].at[0,"first_name"], disabled=False, key="input_first_name")
                        new_email = st.text_input("Novo Email", value=st.session_state["df_employee_upd"].at[0,"email"], disabled=False, key="input_email")   
                        new_hire_date = st.date_input("Nova Data de Contratação", value=st.session_state["df_employee_upd"].at[0,"hire_date"], disabled=False, key="input_hire_date")
                        new_birth_date = st.date_input("Nova Data de Nascimento", value=st.session_state["df_employee_upd"].at[0,"birth_date"], disabled=False, key="input_birth_date")
                        new_department_id = st.number_input("Novo ID do Departamento", min_value=1, step=1, value=st.session_state["df_employee_upd"].at[0,"department_id"], disabled=False, key="input_department_id")
                        new_job_title = st.text_input("Novo Cargo", value=st.session_state["df_employee_upd"].at[0,"job_title"], disabled=False, key="input_job_title")
                        new_gender = st.selectbox("Novo Gênero", gender_options, index=gender_index, disabled=False, key="input_gender")
                        new_nationality = st.text_input("Nova Nacionalidade", value=st.session_state["df_employee_upd"].at[0,"nationality"], disabled=False, key="input_nationality")
                    with col2:
                        new_last_name = st.text_input("Novo Sobrenome", value=st.session_state["df_employee_upd"].at[0,"last_name"], disabled=False, key="input_last_name")      
                        new_phone_number = st.text_input("Novo Número de Telefone", value=st.session_state["df_employee_upd"].at[0,"phone_number"], disabled=False, key="input_phone_number")   
                        new_termination_date = st.date_input("Nova Data de Terminação", value=termination_date, disabled=False, key="input_termination_date")
                        new_start_date = st.date_input("Nova Data de Início", value=st.session_state["df_employee_upd"].at[0,"start_date"], disabled=False, key="input_start_date")
                        new_manager_id = st.number_input("Novo ID do Gerente", min_value=1, step=1, value=st.session_state["df_employee_upd"].at[0,"manager_id"], disabled=False, key="input_manager_id")
                        new_salary = st.number_input("Novo Salário", min_value=0.01, format="%.2f", value=st.session_state["df_employee_upd"].at[0,"salary"], disabled=False, key="input_salary")
                        new_location = st.text_input("Nova Localização", value=st.session_state["df_employee_upd"].at[0,"location"], disabled=False, key="input_location")
                                        

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

    def supplier(self):
        st.title("Gerenciamento de Fornecedores")

        # Adicionar Fornecedor
        with st.expander("Adicionar um Novo Fornecedor"):
            with st.form("new_supplier"):
                company_name = st.text_input("Nome da Empresa")
                contact_name = st.text_input("Nome do Contato")
                email = st.text_input("Email")
                phone_number = st.text_input("Número de Telefone")
                website = st.text_input("Website")
                address = st.text_area("Endereço")
                product_categories = st.selectbox(
                    "Categorias de produtos ou serviços fornecidos",
                    options=["Categoria 1", "Categoria 2", "Categoria 3"]
                )
                primary_product = st.text_input("Descrição do Produto ou Serviço contratado")
                submit_button = st.form_submit_button("Adicionar Fornecedor")

                if submit_button:
                    response = requests.post(
                        "http://backend:8000/suppliers/",
                        json={
                            "company_name": company_name,
                            "contact_name": contact_name,
                            "email": email,
                            "phone_number": phone_number,
                            "website": website,
                            "address": address,
                            "product_categories": product_categories,
                            "primary_product": primary_product,
                        },
                    )
                    self.show_response_message(response)

        # Visualizar Fornecedores
        with st.expander("Visualizar Fornecedores"):
            if st.button("Exibir Todos os Fornecedores"):
                response = requests.get("http://backend:8000/suppliers/")
                if response.status_code == 200:
                    suppliers = response.json()
                    df = pd.DataFrame(suppliers)
                    st.dataframe(df, hide_index=True, width=None)
                else:
                    self.show_response_message(response)

        # Obter Detalhes de um Fornecedor
        with st.expander("Obter Detalhes de um Fornecedor"):
            options = ["Selecione uma opção:", "ID", "Nome Empresa", "Nome Produto"]
            select_search = st.selectbox("Buscar por:", options=options)

            # Determina o estado do campo de entrada de texto
            input_disabled = select_search == "Selecione uma opção:"

            # Determina a mensagem do text_input
            if input_disabled == True:
                mensagem = "Selecione uma opção de pesquisa"
            else:
                mensagem = f"Pesquisar Fornecedor por {select_search}:"

            # Entrada de texto para pesquisa
            search_field = st.text_input(mensagem, disabled=input_disabled)

            search_supplier_bt = st.button("Buscar fornecedor" , disabled=input_disabled)

            if search_supplier_bt:
                # Filtrando o DataFrame com base na entrada do usuário
                if search_field.strip() == "":
                    st.warning("Digite uma valor para ser pesquisado!")
                else:
                    if not input_disabled and search_field:
                        response = requests.get(f"http://backend:8000/suppliers/")

                        if response.status_code == 200:
                            supplier = response.json()
                            df = pd.DataFrame(supplier)
                            
                            if select_search == "Nome Empresa":
                                df_supplier = df[df['company_name'].str.contains(search_field, case=False, na=False)]
                            elif select_search == "Nome Produto":
                                df_supplier = df[df['primary_product'].str.contains(search_field, case=False, na=False)]
                            else:  # Assuming 'ID'
                                df_supplier = df[df['supplier_id'].astype(str).str.contains(search_field, case=False, na=False)]
                                
                            if not df_supplier.empty:
                                st.dataframe(df_supplier, hide_index=True, width=None)
                            else:
                                st.warning("Nenhum Fornecedor encontrado!")
                        else:
                            self.show_response_message(response)

        # Deletar Fornecedor
        with st.expander("Deletar Fornecedor"):
            delete_id = st.number_input("ID do Fornecedor para Deletar", min_value=1, format="%d")
            
            # Botão para consultar Fornecedor
            if st.button("Buscar Fornecedor"):
                response = requests.get(f"http://backend:8000/suppliers/{delete_id}")
                if response.status_code == 200:
                    suppliers = response.json()
                    df = pd.DataFrame([suppliers])
            
                    # Seleciona as colunas desejadas
                    df = df[
                        [
                            "supplier_id",
                            "company_name",
                            "contact_name",
                            "primary_product",
                            "email",
                            "phone_number"
                        ]
                    ]

                    # Salvando o funcionário encontrado no estado da sessão
                    st.session_state['df_suppliers_del'] = df
                    st.session_state['id_suppliers_del'] = delete_id
                else:
                    st.warning("Fornecedor não encontrado!")
                    st.session_state.pop('df_suppliers_del', None)
            
            # Exibe as informações do Fornecedor, se encontrado
            if 'df_suppliers_del' in st.session_state:    
                st.text_input("Nome da Empresa:", value=st.session_state["df_suppliers_del"].at[0, "company_name"], disabled=True, key="input_company_name")
                st.text_input("Nome de Contato:", value=st.session_state["df_suppliers_del"].at[0, "contact_name"], disabled=True, key="input_contact_name")
                st.text_input("Produto:", value=st.session_state["df_suppliers_del"].at[0, "primary_product"], disabled=True, key="input_primary_product")
                st.text_input("E-mail:", value=st.session_state["df_suppliers_del"].at[0, "email"], disabled=True, key="input_email")
                st.text_input("Telefone:", value=st.session_state["df_suppliers_del"].at[0, "phone_number"], disabled=True, key="input_phone")     

                # Botão para deletar funcionário
                if st.button("Deletar Fornecedor"):
                    response = requests.delete(f"http://backend:8000/suppliers/{st.session_state['id_suppliers_del']}")
                    if response.status_code == 200:
                        st.success("Fornecedor deletado com sucesso!")
                        st.session_state.pop('df_suppliers_del')
                        st.session_state.pop('id_suppliers_del')
                    else:
                        st.error("Erro ao deletar o Fornecedor!")


        # Atualizar Fornecedor
        with st.expander("Atualizar Fornecedor"):
            with st.form("update_supplier"):
                update_id = st.number_input("ID do Fornecedor", min_value=1, format="%d")
                new_company_name = st.text_input("Novo Nome da Empresa")
                new_contact_name = st.text_input("Novo Nome do Contato")
                new_email = st.text_input("Novo Email")
                new_phone_number = st.text_input("Novo Número de Telefone")
                new_website = st.text_input("Novo Website")
                new_address = st.text_area("Novo Endereço")
                new_product_categories = st.selectbox(
                    "Categorias de produtos ou serviços fornecidos",
                    options=["Categoria 1", "Categoria 2", "Categoria 3"]
                )
                new_primary_product = st.text_input("Nova descrição do Produto ou Serviço contratado")

                update_button = st.form_submit_button("Atualizar Fornecedor")

                if update_button:
                    update_data = {}
                    if new_company_name:
                        update_data["company_name"] = new_company_name
                    if new_contact_name:
                        update_data["contact_name"] = new_contact_name
                    if new_email:
                        update_data["email"] = new_email
                    if new_phone_number:
                        update_data["phone_number"] = new_phone_number
                    if new_website:
                        update_data["website"] = new_website
                    if new_address:
                        update_data["address"] = new_address
                    if new_product_categories:
                        update_data["product_categories"] = new_product_categories
                    if new_primary_product:
                        update_data["primary_product"] = new_primary_product

                    if update_data:
                        response = requests.put(
                            f"http://backend:8000/suppliers/{update_id}", json=update_data
                        )
                        self.show_response_message(response)
                    else:
                        st.error("Nenhuma informação fornecida para atualização")

    def sales(self):
        st.title("Gerenciamento de Vendas")
        
        # Adicionar Venda
        with st.expander("Adicionar uma Nova Venda"):
            with st.form("new_sale"):
                email = st.text_input("Email do Vendedor")
                data = st.date_input("Data da compra", datetime.now())
                hora = st.time_input("Hora da compra", value=time(9, 0))
                valor = st.number_input("Valor da venda", min_value=0.0, format="%.2f")
                quantidade = st.number_input("Quantidade de produtos", min_value=1, step=1)
                produto = st.selectbox("Produto", options=["ZapFlow com Gemini", "ZapFlow com chatGPT", "ZapFlow com Llama3.0"])
                
                submit_button = st.form_submit_button("Adicionar Venda")

                if submit_button:
                    data_hora = datetime.combine(data, hora)
                    response = requests.post(
                        "http://backend:8000/sales/",
                        json={
                            "email": email,
                            "data": data_hora.isoformat(),
                            "valor": valor,
                            "quantidade": quantidade,
                            "produto": produto,
                        },
                    )
                    self.show_response_message(response)

        # Visualizar Vendas
        with st.expander("Visualizar Vendas"):
            if st.button("Exibir Todas as Vendas"):
                response = requests.get("http://backend:8000/sales/")
                if response.status_code == 200:
                    sales = response.json()
                    df = pd.DataFrame(sales)
                    st.dataframe(df, hide_index=True, width=None)
                else:
                    self.show_response_message(response)

        # Obter Detalhes de uma Venda
        with st.expander("Obter Detalhes de uma Venda"):
            options = ["Selecione uma opção:", "ID", "Email", "Produto", "Data"]
            select_search = st.selectbox("Buscar por:", options=options)

            # Determina o estado do campo de entrada de texto
            input_disabled = select_search == "Selecione uma opção:"

            # Determina a mensagem do text_input
            if input_disabled == True:
                mensagem = "Selecione uma opção de pesquisa"
            else:
                mensagem = f"Pesquisar Venda por {select_search}:"

            if select_search == 'Data':
                search_field = st.date_input("Selecione a Data da Venda", datetime.now())
            else:
                # Entrada de texto para pesquisa
                search_field = st.text_input(mensagem, disabled=input_disabled)

            search_supplier_bt = st.button("Buscar venda" , disabled=input_disabled)

            if search_supplier_bt:
                # Filtrando o DataFrame com base na entrada do usuário
                if isinstance(search_field, str) and search_field.strip() == "":
                    st.warning("Digite um valor para ser pesquisado!")
                else:
                    if not input_disabled and search_field:
                        response = requests.get(f"http://backend:8000/sales/")

                        if response.status_code == 200:
                            sales = response.json()
                            df = pd.DataFrame(sales)
                            
                            if select_search == "Email":
                                df_sales = df[df['email'].str.contains(search_field, case=False, na=False)]
                            elif select_search == "Produto":
                                df_sales = df[df['produto'].str.contains(search_field, case=False, na=False)]
                            elif select_search == "Data":
                                search_field_str = search_field.strftime('%Y-%m-%d')
                                df_sales = df[df['data'].str.contains(search_field_str, case=False, na=False)]
                            else:  # Assuming 'ID'
                                df_sales = df[df['id'].astype(str).str.contains(search_field, case=False, na=False)]
                                
                            if not df_sales.empty:
                                st.dataframe(df_sales, hide_index=True, width=None)
                            else:
                                st.warning("Nenhuma Venda encontrada!")
                        else:
                            self.show_response_message(response)

        # Deletar Venda
        with st.expander("Deletar Venda"):
            delete_id = st.number_input("ID da Venda para Deletar", min_value=1, format="%d")
            if st.button("Deletar Venda"):
                response = requests.delete(f"http://backend:8000/sales/{delete_id}")
                self.show_response_message(response)

        # Atualizar Venda
        with st.expander("Atualizar Venda"):
            with st.form("update_sale"):
                update_id = st.number_input("ID da Venda", min_value=1, format="%d")
                new_email = st.text_input("Novo Email do Vendedor")
                new_data = st.date_input("Nova Data da compra")
                new_hora = st.time_input("Nova Hora da compra")
                new_valor = st.number_input("Novo Valor da venda", min_value=0.0, format="%.2f")
                new_quantidade = st.number_input("Nova Quantidade de produtos", min_value=1, step=1)
                new_produto = st.selectbox("Novo Produto", options=["ZapFlow com Gemini", "ZapFlow com chatGPT", "ZapFlow com Llama3.0"])

                update_button = st.form_submit_button("Atualizar Venda")

                if update_button:
                    update_data = {}
                    if new_email:
                        update_data["email"] = new_email
                    if new_data and new_hora:
                        update_data["data"] = datetime.combine(new_data, new_hora).isoformat()
                    if new_valor > 0:
                        update_data["valor"] = new_valor
                    if new_quantidade > 0:
                        update_data["quantidade"] = new_quantidade
                    if new_produto:
                        update_data["produto"] = new_produto

                    if update_data:
                        response = requests.put(
                            f"http://backend:8000/sales/{update_id}", json=update_data
                        )
                        self.show_response_message(response)
                    else:
                        st.error("Nenhuma informação fornecida para atualização")
    
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

        st.image("https://raw.githubusercontent.com/tsffarias/LiftOff_Data/refs/heads/main/img/arquitetura_1.2.png", use_column_width=True, caption="Arquitetura do Pipeline de Dados")

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
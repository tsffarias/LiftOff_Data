<h1 align="center">📊 LiftOff Data</h1> 
<div align="center">
    <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" target="_blank"></a>
    <a href="https://www.postgresql.org/docs/" target="_blank"><img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white" target="_blank"></a>
    <a href="https://fastapi.tiangolo.com/" target="_blank"><img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" target="_blank"></a>
    <a href="https://streamlit.io/" target="_blank"><img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" target="_blank"></a>
    <a href="https://www.sqlalchemy.org/" target="_blank"><img src="https://img.shields.io/badge/SQLAlchemy-323232?style=for-the-badge&logo=sqlalchemy&logoColor=white" target="_blank"></a>
    <a href="https://pydantic-docs.helpmanual.io/" target="_blank"><img src="https://img.shields.io/badge/Pydantic-3776AB?style=for-the-badge&logo=pydantic&logoColor=white" target="_blank"></a>
    <a href="https://docs.docker.com/" target="_blank"><img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" target="_blank"></a>
</div>


> Este projeto apresenta uma arquitetura de pipeline de dados de baixo custo, projetada para startups que precisam processar e analisar dados de vendas de forma eficiente.

---

### **Introdução**

Este projeto descreve uma arquitetura de pipeline de dados de baixo custo voltada para startups, com foco em integração de dados de vendas a partir de APIs e CRMs, utilizando tecnologias modernas e acessíveis. O objetivo é criar uma solução escalável para ingestão, transformação e visualização de dados, garantindo que tanto engenheiros de dados quanto analistas possam colaborar eficientemente. A arquitetura proposta inclui a divisão do pipeline em múltiplas camadas (Bronze, Silver e Gold), integração com APIs, Kafka para streaming, Airbyte para ingestão de dados, Airflow para orquestração e DBT para transformação de dados. A plataforma colaborativa "Briefer" também é integrada, permitindo que analistas de dados acessem e utilizem os dados transformados de forma eficiente.

<p align="center">
<img src = "./img/arquitetura_1.2.png">
</p>

### **Sequence Diagram**

O diagrama abaixo ilustra a interação entre as principais camadas e componentes da arquitetura, desde a ingestão dos dados brutos até sua transformação e disponibilização para análise.
```mermaid
sequenceDiagram
    participant U as Usuário
    participant SW as Sistema Web Streamlit
    participant V as Validação Pydantic
    participant DB as Banco de Dados SQLAlchemy
    
    U ->> SW: Inserir Dados
    SW ->> V: Enviar Dados para Validação
    alt Dados Válidos
        V ->> DB: Inserir Dados no Banco de Dados
        DB ->> SW: Confirmação de Armazenamento
        SW ->> U: Dados Salvos com Sucesso
    else Dados Inválidos
        V ->> SW: Retornar Erros de Validação
        SW ->> U: Exibir Mensagem de Erro
    end
```

O diagrama a seguir descreve o fluxo de dados desde a entrada do usuário no frontend até a validação dos dados e o salvamento no banco de dados, se aprovado.

```mermaid
graph TD
    A[Usuário Digita no Frontend] --> B{Validação do Contrato de Dados}
    
    B -- Dados Válidos --> C[Salva no Banco de Dados]
    B -- Dados Inválidos --> D[Erro de Validação Exibido]

    A --> |Entrada de Dados| B
    B --> |Validação pelo Pydantic| C
    B --> |Falha na Validação| D
    C --> E[Dados Salvos com Sucesso]
    D --> F[Mostrar Mensagem de Erro no Frontend]
```

---

### **Tecnologias Utilizadas**

#### **Streamlit**

- **Descrição:** Streamlit é uma biblioteca Python de código aberto que permite a criação de aplicativos web interativos de forma rápida e fácil. Utilizado principalmente para construir dashboards e interfaces de dados, o Streamlit é ideal para prototipagem rápida e visualização de dados sem a necessidade de conhecimentos avançados em desenvolvimento web.
- **Uso no Projeto:** Utilizado para construir o frontend da aplicação, permitindo que os usuários insiram dados de vendas de forma interativa e visualizem os resultados diretamente na interface.

#### **Pydantic**

- **Descrição:** Pydantic é uma biblioteca de validação de dados que utiliza modelos baseados em classes Python para garantir que os dados inseridos estejam no formato correto. É amplamente utilizada para validação e serialização de dados, garantindo integridade e consistência.
- **Uso no Projeto:** Pydantic é utilizado para validar os dados inseridos pelos usuários no frontend, garantindo que as informações estejam corretas antes de serem processadas e salvas no banco de dados.

#### **Psycopg2**

- **Descrição:** Psycopg2 é uma biblioteca que permite a interação com bancos de dados PostgreSQL diretamente através de Python, facilitando a execução de comandos SQL e o gerenciamento das conexões.
- **Uso no Projeto:** Utilizado para conectar a aplicação ao banco de dados PostgreSQL, executar comandos SQL, e salvar os dados validados.

#### **SQLAlchemy**

- **Descrição:** SQLAlchemy é uma poderosa biblioteca de SQL toolkit e ORM (Object-Relational Mapping) para Python. Ele permite a interação com bancos de dados relacionais de forma mais intuitiva, utilizando objetos Python em vez de comandos SQL diretamente.
- **Uso no Projeto:** SQLAlchemy foi utilizado para gerenciar a conexão com o banco de dados PostgreSQL e facilitar as operações de CRUD.

#### **MkDocs**

- **Descrição:** MkDocs é uma ferramenta estática de documentação em Python que permite a criação de sites de documentação de forma simples e estruturada. É especialmente útil para projetos que precisam de uma documentação clara e acessível para os desenvolvedores e usuários.
- **Uso no Projeto:** MkDocs é utilizado para gerar a documentação do sistema, detalhando como o projeto foi estruturado, as funcionalidades desenvolvidas, e como o sistema deve ser mantido e atualizado.
- **Configuração e Execução:**
  1. Para visualizar a documentação localmente, execute: `mkdocs serve`
  2. Acesse a documentação em: `http://127.0.0.1:8000/`

<p align="center">
  <img src = "./img/mkdocs.png">
</p>

#### **MinIO**
- **Descrição:** MinIO é uma solução de armazenamento de objetos de código aberto compatível com o protocolo Amazon S3, ideal para o armazenamento escalável de grandes volumes de dados. Ele permite o uso local de serviços de armazenamento distribuído para dados não estruturados, como arquivos, logs e objetos de dados.
- **Uso no Projeto:** No contexto deste projeto, MinIO é utilizado para armazenar dados brutos de produtos, funcionarios e fornecedores, por exempo: imagens, documentos em pdf. Ele serve como a camada de armazenamento persistente dos dados nas fases de ingestão e transformação.

#### **Airbyte**

- **Descrição:** Airbyte é uma plataforma de integração de dados de código aberto que permite conectar facilmente APIs, bancos de dados e outros sistemas para ingestão de dados em tempo real.
- **Uso no Projeto:** Responsável pela ingestão de dados a partir de diferentes APIs e fontes de dados, garantindo que os dados sejam movidos para as camadas corretas do pipeline.

#### **Kafka**

- **Descrição:** Apache Kafka é uma plataforma de streaming distribuída que permite a publicação e assinatura de fluxos de dados em tempo real.
- **Uso no Projeto:** Utilizado para gerenciar o fluxo de dados de maneira escalável e garantir que os dados sejam processados de forma contínua e eficiente.

#### **Airflow**

- **Descrição:** Apache Airflow é uma plataforma de orquestração de workflows que permite o agendamento e monitoramento de pipelines de dados.
- **Uso no Projeto:** Orquestra a execução de todos os componentes do pipeline, desde a ingestão até a transformação dos dados.

#### **DBT**

- **Descrição:** DBT (Data Build Tool) é uma ferramenta de transformação de dados que permite a construção de modelos SQL e a aplicação de boas práticas de desenvolvimento de software ao ETL.
- **Uso no Projeto:** Utilizado para transformar os dados das camadas Bronze e Silver, preparando-os para a camada Gold, onde estarão prontos para consumo pelos analistas.

#### **Briefer**

- **Descrição:** Briefer é uma plataforma colaborativa de dados que permite que equipes de analistas acessem, compartilhem e analisem dados de maneira colaborativa.
- **Uso no Projeto:** Facilita o acesso e a exploração dos dados transformados pelos analistas, proporcionando um ambiente colaborativo para análise de dados.

<p align="center">
<img src = "./img/briefer.png">
</p>

---

### **Estrutura do Projeto**

#### **Divisão dos Módulos**

O projeto está dividido em módulos para organizar melhor o desenvolvimento e facilitar a manutenção futura. A seguir, estão os principais módulos do projeto:

1. **Frontend (`app.py`):**
   - Responsável pela interface do usuário onde os dados de vendas são inseridos e exibidos.
   - Desenvolvido com Streamlit para proporcionar uma interação simples e amigável.

2. **Contrato (`<model_name>_schema.py.py`):**
   - Define as regras de validação dos dados utilizando Pydantic.
   - Assegura que os dados inseridos no frontend estão no formato correto e cumprem as regras estabelecidas pelo sistema.

3. **Banco de Dados (`database.py`):**
   - Gerencia a conexão e as operações com o banco de dados PostgreSQL utilizando Psycopg2.
   - Facilita a interação com o banco sem a necessidade de escrever SQL diretamente.

### Diagrama de Fluxo das Camadas Bronze, Silver e Gold no DBT

O pipeline de dados é dividido em três camadas principais para garantir a qualidade e integridade dos dados à medida que eles progridem no sistema:

```mermaid
graph TD
    A[Raw Data Source] -->|Extrai dados brutos| B[Bronze Layer]
    B[Bronze Layer] -->|Limpeza de dados| C[Silver Layer]
    C[Silver Layer] -->|Agregação e cálculos| D[Gold Layer - Vendas por Produto]
    C[Silver Layer] -->|Agregação e cálculos| E[Gold Layer - Vendas por Vendedor]
    
    subgraph Bronze
        B1[bronze_vendas.sql]
    end
    
    subgraph Silver
        S1[silver_vendas.sql]
    end
    
    subgraph Gold
        G1[gold_vendas_7_dias.sql]
        G2[gold_vendas_por_vendedor.sql]
    end
```

### Explicação do Diagrama

- **Bronze Layer:** Esta camada recebe os dados brutos diretamente das fontes, criando uma visualização inicial sem transformações significativas.
  
- **Silver Layer:** Nesta etapa, os dados são limpos, ajustando datas inválidas e removendo outliers. É a fase em que os dados começam a ser preparados para análise.

- **Gold Layer:** Dados finais prontos para análise e visualização, acessíveis por ferramentas como o Briefer.
  - **Gold Vendas por Produto:** Agrega e calcula os dados para apresentar o desempenho dos produtos nos últimos 7 dias.
  - **Gold Vendas por Vendedor:** Apresenta o desempenho dos vendedores, também focando nos últimos 7 dias.

---

### **Passos para Configuração e Execução**

## Instalação via docker
Antes de rodar o Docker, crie um arquivo .env na raiz do projeto com os seguintes valores:

```
DB_HOST_PROD = postgres
DB_PORT_PROD = 5432
DB_NAME_PROD = mydatabase
DB_USER_PROD = user
DB_PASS_PROD = password
PGADMIN_EMAIL = email_pgadmin
PGADMIN_PASSWORD = password_pgadmin
```

Para iniciar a aplicação, execute:

```bash
docker-compose up -d --build
```

#### **1. Criar o Repositório**

- **Passo:** Inicie um novo repositório no GitHub ou GitLab para versionar o projeto.
- **Comando:**
  ```bash
  git init
  ```

#### **2. Escolher a Versão do Python para 3.12.3**

- Utilize `pyenv` para gerenciar e definir a versão correta do Python:
  ```bash
  pyenv install 3.12.3
  pyenv local 3.12.3
  ```

#### **3. Criar um Ambiente Virtual**

- **Passo:** Crie um ambiente virtual para isolar as dependências do projeto.
- **Comando:**
  ```bash
  python3.12 -m venv .venv
  ```

#### **4. Entrar no Ambiente Virtual**

- **Comando:**
  - **Windows:**
    ```bash
    .venv\Scripts\activate
    ```
  - **Linux/Mac:**
    ```bash
    source .venv/bin/activate
    ```

#### **5. Instalar as Dependências**

- **Instalar os pacotes necessários:**
  ```bash
  pip install -r requirements.txt
  ```

#### **6. Executar o Frontend**

- **Comando para rodar o frontend com Streamlit:**
  ```bash
  streamlit run app.py
  ```

#### **7. Configurar o PostgreSQL**

- **Criar o banco de dados e a tabela necessária:**
  ```sql
  CREATE DATABASE crm_vendas;
  CREATE TABLE vendas (
      id SERIAL PRIMARY KEY,
      email VARCHAR(255) NOT NULL,
      data TIMESTAMP NOT NULL,
      valor NUMERIC NOT NULL,
      quantidade INTEGER NOT NULL,
      produto VARCHAR(50) NOT NULL
  );
  ```

#### **8. Criar a Conexão com o PostgreSQL**

- A conexão é gerenciada no módulo `database.py` utilizando `psycopg2`.

### **Conclusão**

Este projeto de arquitetura de pipeline de dados para startups oferece uma solução eficiente, escalável e de baixo custo para lidar com o processamento e análise de grandes volumes de dados de vendas. Com a utilização de ferramentas modernas como Airbyte, Kafka, Airflow, DBT e Briefer, o pipeline garante a ingestão, transformação e disponibilização dos dados em camadas organizadas (Bronze, Silver, Gold), permitindo uma análise colaborativa e em tempo real.

Essa arquitetura modular e flexível facilita a adaptação e o crescimento conforme a demanda aumenta, tornando-se uma excelente escolha para startups que precisam otimizar seus processos de dados sem comprometer o orçamento.


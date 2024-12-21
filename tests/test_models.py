import pytest
from datetime import date
from pydantic import ValidationError
from app.backend.models.product.product_schema import ProductCreate
from app.backend.models.employee.employee_schema import EmployeeCreate
from app.backend.models.supplier.supplier_schema import SupplierCreate

def test_product_com_dados_validos():
    dados_validos = {
        "name": "Notebook",
        "description": "Notebook ultrafino",
        "price": 2999.99,
        "categoria": "Eletrônico",
        "email_fornecedor": "fornecedor@example.com"
    }

    produto = ProductCreate(**dados_validos)

    assert produto.name == dados_validos["name"]
    assert produto.description == dados_validos["description"]
    assert produto.price == dados_validos["price"]
    assert produto.categoria == dados_validos["categoria"]
    assert produto.email_fornecedor == dados_validos["email_fornecedor"]


def test_product_com_dados_invalidos():
    dados_invalidos = {
        "name": "Notebook",
        "description": "Notebook ultrafino",
        "price": -100,  # Valor negativo inválido
        "categoria": "Inexistente",  # Categoria inválida
        "email_fornecedor": "fornecedor"  # Email inválido
    }

    with pytest.raises(ValidationError):
        ProductCreate(**dados_invalidos)


def test_employee_com_dados_validos():
    dados_validos = {
        "first_name": "Maria",
        "last_name": "Souza",
        "email": "maria.souza@example.com",
        "phone_number": "11999999999",
        "hire_date": date.today(),
        "department_id": 10,
        "manager_id": 2,
        "job_title": "Analista de Dados",
        "location": "São Paulo, Brasil",
        "birth_date": date(1990, 5, 20),
        "gender": "Masculino",  # Campo string conforme schema
        "nationality": "Brasileira",
        "start_date": date.today(),
        "salary": 5000.0,
        "termination_date": None
    }

    funcionario = EmployeeCreate(**dados_validos)

    assert funcionario.first_name == dados_validos["first_name"]
    assert funcionario.last_name == dados_validos["last_name"]
    assert funcionario.email == dados_validos["email"]
    assert funcionario.phone_number == dados_validos["phone_number"]
    assert funcionario.hire_date == dados_validos["hire_date"]
    assert funcionario.department_id == dados_validos["department_id"]
    assert funcionario.manager_id == dados_validos["manager_id"]
    assert funcionario.job_title == dados_validos["job_title"]
    assert funcionario.location == dados_validos["location"]
    assert funcionario.birth_date == dados_validos["birth_date"]
    assert funcionario.gender == dados_validos["gender"]
    assert funcionario.nationality == dados_validos["nationality"]
    assert funcionario.start_date == dados_validos["start_date"]
    assert funcionario.salary == dados_validos["salary"]
    assert funcionario.termination_date == dados_validos["termination_date"]


def test_employee_com_dados_invalidos():
    dados_invalidos = {
        "first_name": "Maria",
        "last_name": "Souza",
        "email": "maria.souza",  # Email inválido
        "phone_number": "11999999999",
        "hire_date": "não é uma data",
        "department_id": 10,
        "manager_id": 2,
        "job_title": "Analista de Dados",
        "location": "São Paulo, Brasil",
        "birth_date": "não é uma data",
        "gender": "Inexistente", # Não há validação direta, mas poderia ter
        "nationality": "Brasileira",
        "start_date": "não é uma data",
        "salary": -1000.0, # Valor negativo
        "termination_date": "não é uma data"
    }

    with pytest.raises(ValidationError):
        EmployeeCreate(**dados_invalidos)


def test_supplier_com_dados_validos():
    dados_validos = {
        "company_name": "Fornecedor LTDA",
        "contact_name": "Carlos",
        "email": "contato@fornecedor.com",
        "phone_number": "11988888888",
        "website": "https://fornecedor.com",
        "address": "Rua A, 123",
        "product_categories": "Categoria 1",
        "primary_product": "Peças de Computador"
    }

    fornecedor = SupplierCreate(**dados_validos)

    assert fornecedor.company_name == dados_validos["company_name"]
    assert fornecedor.contact_name == dados_validos["contact_name"]
    assert fornecedor.email == dados_validos["email"]
    assert fornecedor.phone_number == dados_validos["phone_number"]
    assert fornecedor.website == dados_validos["website"]
    assert fornecedor.address == dados_validos["address"]
    assert fornecedor.product_categories == dados_validos["product_categories"]
    assert fornecedor.primary_product == dados_validos["primary_product"]


def test_supplier_com_dados_invalidos():
    dados_invalidos = {
        "company_name": "Fornecedor LTDA",
        "contact_name": "Carlos",
        "email": "contato",  # Email inválido
        "phone_number": "11988888888",
        "website": "https://fornecedor.com",
        "address": "Rua A, 123",
        "product_categories": "Categoria Inexistente", # Categoria inválida
        "primary_product": "Peças de Computador"
    }

    with pytest.raises(ValidationError):
        SupplierCreate(**dados_invalidos)

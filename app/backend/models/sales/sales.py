from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database.database import Base


class SalesModel(Base):
    """
    Modelo de dados para representar uma venda no banco de dados.

    Atributos:
        id (Integer): Identificador único da venda, chave primária.
        email_employee (EmailStr): email do funcionario
        email_customer (EmailStr): email do comprador
        first_name (str): Primeiro nome do comprador
        last_name (str): Ultimo nome do comprador   
        phone_number (str): Número de telefone do comprador
        price (Float): Valor total da venda.
        quantity (Integer): Quantidade de itens vendidos.
        name_product (String): Nome ou identificador do produto vendido.
        date (datetime): Data e hora da venda.
        created_at (DateTime): Data e hora de criação do registro da venda.
    """

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email_employee = Column(String, index=True)
    email_customer = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    phone_number = Column(String, index=True)
    price = Column(Float, index=True)
    quantity = Column(Integer, index=True)
    name_product = Column(String, index=True)
    date = Column(DateTime(timezone=True), index=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)    
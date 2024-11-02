from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database.database import Base


class SalesModel(Base):
    """
    Modelo de dados para representar uma venda no banco de dados.

    Atributos:
        id (Integer): Identificador único da venda, chave primária.
        email (String): Email do comprador.
        valor (Float): Valor total da venda.
        quantidade (Integer): Quantidade de itens vendidos.
        produto (String): Nome ou identificador do produto vendido.
        data (DateTime): Data e hora da venda.
        created_at (DateTime): Data e hora de criação do registro da venda.
    """

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String, index=True)
    valor = Column(Float, index=True)
    quantidade = Column(Integer, index=True)
    produto = Column(String, index=True)
    data = Column(DateTime(timezone=True), index=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)
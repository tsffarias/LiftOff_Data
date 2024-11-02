from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database.database import Base


class ProductModel(Base):
    """
    Modelo de dados para representar um produto no banco de dados.

    Atributos:
        id (Integer): Identificador único do produto, chave primária.
        name (String): Nome do produto.
        description (String): Descrição do produto.
        price (Float): Preço do produto.
        categoria (String): Categoria do produto.
        email_fornecedor (String): Email do fornecedor do produto.
        created_at (DateTime): Data e hora de criação do registro do produto.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    categoria = Column(String, index=True)
    email_fornecedor = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)
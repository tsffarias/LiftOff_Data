
from sqlalchemy import Column, Integer, String, DateTime, ARRAY
from sqlalchemy.sql import func
from database.database import Base

class SupplierModel(Base):
    """
    Modelo de dados para representar um fornecedor no banco de dados.

    Atributos:
        supplier_id (Integer): Identificador único do fornecedor, chave primária.
        company_name (String): Nome da empresa fornecedora.
        contact_name (String): Nome do contato principal.
        email (String): Endereço de email.
        phone_number (String): Número de telefone.
        website (String): Website da empresa.
        address (String): Endereço completo.
        product_categories (String): Lista de categorias de produtos ou serviços fornecidos.
        primary_product (String): Produto ou serviço principal.
        created_at (DateTime): Data e hora de criação do registro do fornecedor.
    """

    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True, nullable=False)
    contact_name = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False)
    phone_number = Column(String, nullable=False)
    website = Column(String)
    address = Column(String)
    product_categories = Column(String, index=True)    
    primary_product = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)

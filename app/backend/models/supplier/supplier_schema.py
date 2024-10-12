from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum

class ProductCategoriesEnum(str, Enum):
    produto1 = "Categoria 1"
    produto2 = "Categoria 2"
    produto3 = "Categoria 3"

class SupplierBase(BaseModel):
    """
    Modelo de dados para fornecedores.

    Args:
        supplier_id (int): Identificador único do fornecedor (chave primária)
        company_name (str): Nome da empresa fornecedora
        contact_name (str): Nome do contato principal
        email (EmailStr): Endereço de email
        phone_number (str): Número de telefone
        website (str): Website da empresa
        address (str): Endereço completo
        product_categories (List[ProdutoEnum]): Categorias dos produtos ou serviços fornecidos
        primary_product (str): Produto ou serviço principal
    """
    
    supplier_id: int
    company_name: str
    contact_name: str
    email: EmailStr
    phone_number: str
    website: str
    address: str
    product_categories: ProductCategoriesEnum
    primary_product: str

    @field_validator("product_categories", mode="before")
    @classmethod
    def check_categoria(cls, v):
        if v in [item.value for item in ProductCategoriesEnum]:
            return v
        raise ValueError("Categoria inválida")

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SupplierUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    product_categories: Optional[str] = None
    primary_product: Optional[str] = None

    @field_validator("product_categories", mode='before')
    def check_categoria(cls, v):
        if v is None:
            return v
        if v in [item.value for item in ProductCategoriesEnum]:
            return v
        raise ValueError("Categoria inválida")
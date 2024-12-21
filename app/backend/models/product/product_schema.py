from pydantic import BaseModel, PositiveFloat, EmailStr, field_validator, Field, ConfigDict
from enum import Enum
from datetime import datetime
from typing import Optional


class CategoriaBase(Enum):
    """
    Enum representando as categorias de produtos.
    """
    categoria1 = "Eletrônico"
    categoria2 = "Eletrodoméstico"
    categoria3 = "Móveis"
    categoria4 = "Roupas"
    categoria5 = "Calçados"


class ProductBase(BaseModel):
    """
    Modelo base para informações do produto.

    Atributos:
        name (str): O nome do produto.
        description (Optional[str]): Uma descrição opcional do produto.
        price (PositiveFloat): O preço do produto.
        categoria (str): A categoria do produto.
        email_fornecedor (EmailStr): O email do fornecedor do produto.
    """
    name: str
    description: Optional[str] = None
    price: PositiveFloat
    categoria: str
    email_fornecedor: EmailStr

    @field_validator("categoria")
    @classmethod
    def check_categoria(cls, v):
        """
        Valida a categoria do produto.

        Args:
            v (str): O valor da categoria a ser validado.

        Returns:
            str: O valor da categoria validado.

        Raises:
            ValueError: Se a categoria for inválida.
        """
        if v in [item.value for item in CategoriaBase]:
            return v
        raise ValueError("Categoria inválida")


class ProductCreate(ProductBase):
    """
    Modelo para criar um novo produto. Herda todos os campos de ProductBase.
    """
    pass


class ProductResponse(ProductBase):
    """
    Modelo para resposta de produto, incluindo campos adicionais.

    Atributos:
        id (int): O identificador único do produto.
        created_at (datetime): O timestamp de quando o produto foi criado.
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    """
    Modelo para atualizar um produto existente.

    Atributos:
        name (Optional[str]): O nome atualizado do produto.
        description (Optional[str]): A descrição atualizada do produto.
        price (Optional[PositiveFloat]): O preço atualizado do produto.
        categoria (Optional[str]): A categoria atualizada do produto.
        email_fornecedor (Optional[EmailStr]): O email atualizado do fornecedor do produto.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[PositiveFloat] = None
    categoria: Optional[str] = None
    email_fornecedor: Optional[EmailStr] = None

    @field_validator("categoria", mode='before')
    def check_categoria(cls, v):
        """
        Valida a categoria do produto durante a atualização.

        Args:
            v (Optional[str]): O valor da categoria a ser validado.

        Returns:
            Optional[str]: O valor da categoria validado ou None.

        Raises:
            ValueError: Se a categoria for inválida.
        """
        if v is None:
            return v
        if v in [item.value for item in CategoriaBase]:
            return v
        raise ValueError("Categoria inválida")
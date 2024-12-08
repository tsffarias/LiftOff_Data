from datetime import datetime
from typing import Tuple
from pydantic import BaseModel, EmailStr, PositiveFloat, PositiveInt, field_validator
from enum import Enum
from typing import Optional

class ProdutoEnum(str, Enum):
    produto1 = "ZapFlow com Gemini"
    produto2 = "ZapFlow com chatGPT"
    produto3 = "ZapFlow com Llama3.0"

class SalesBase(BaseModel):
    """
    Modelo de dados para as vendas.

    Args:
        email_employee (EmailStr): email do funcionario
        email_customer (EmailStr): email do comprador
        date (datetime): data da compra
        first_name (str): Primeiro nome do comprador
        last_name (str): Ultimo nome do comprador   
        phone_number (str): Número de telefone do comprador
        price (PositiveFloat): valor da compra
        name_product (PositiveInt): nome do produto
        quantity (PositiveInt): quantidade de produtos
        produto_category (ProdutoEnum): categoria do produto
    """

    email_employee: EmailStr
    email_customer: EmailStr
    first_name: str
    last_name: str    
    phone_number: str
    date: datetime
    price: PositiveFloat
    quantity: PositiveInt
    name_product: str

    '''
    @field_validator("produto_category", mode="before")
    @classmethod
    def check_categoria(cls, v):
        if v in [item.value for item in ProdutoEnum]:
            return v
        raise ValueError("Produto inválido")
    '''
    
class SalesCreate(SalesBase):
    pass

class SalesResponse(SalesBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SalesUpdate(BaseModel):
    email_employee: Optional[EmailStr] = None
    email_customer: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None    
    phone_number: Optional[str] = None
    date: Optional[datetime] = None 
    price: Optional[PositiveFloat] = None
    quantity: Optional[PositiveInt] = None
    name_product: Optional[str] = None

    '''
    @field_validator("name_product", mode='before')
    def check_categoria(cls, v):
        if v is None:
            return v
        if v in [item.value for item in ProdutoEnum]:
            return v
        raise ValueError("Produto inválido")
   '''
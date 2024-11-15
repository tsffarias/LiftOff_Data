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
        email (EmailStr): email do comprador
        data (datetime): data da compra
        valor (PositiveFloat): valor da compra
        produto (PositiveInt): nome do produto
        quantidade (PositiveInt): quantidade de produtos
        produto (ProdutoEnum): categoria do produto
    """

    email: EmailStr
    data: datetime
    valor: PositiveFloat
    quantidade: PositiveInt
    produto: str

    '''
    @field_validator("produto", mode="before")
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
    email: Optional[EmailStr] = None
    data: Optional[datetime] = None 
    valor: Optional[PositiveFloat] = None
    quantidade: Optional[PositiveInt] = None
    produto: Optional[str] = None

    '''
    @field_validator("produto", mode='before')
    def check_categoria(cls, v):
        if v is None:
            return v
        if v in [item.value for item in ProdutoEnum]:
            return v
        raise ValueError("Produto inválido")
   '''
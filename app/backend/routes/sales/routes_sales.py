from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal, get_db
from models.sales.sales_schema import SalesResponse, SalesUpdate, SalesCreate
from typing import List
from crud.sales.crud import (
    create_sales,
    get_sales,
    get_sales_by_id,
    delete_sales,
    update_sales,
)

router = APIRouter()

@router.post("/sales/", response_model=SalesResponse)
def create_sales_route(sales: SalesCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova venda.

    Parâmetros:
    - sales (SalesCreate): Dados da venda a ser criada.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - ProductResponse: Dados do produto criado.
    """
    return create_sales(db=db, sales=sales)


@router.get("/sales/", response_model=List[SalesResponse])
def read_all_sales_route(db: Session = Depends(get_db)):
    """
    Retorna todas as vendas.

    Parâmetros:
    - db (Session): Sessão do banco de dados.

    Retorna:
    - List[ProductResponse]: Lista de todos os produtos.
    """
    sales = get_sales(db)
    return sales


@router.get("/sales/{sales_id}", response_model=SalesResponse)
def read_sales_route(sales_id: int, db: Session = Depends(get_db)):
    """
    Retorna uma venda específica.

    Parâmetros:
    - sales_id (int): ID da venda a ser retornada.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - SalesResponse: Dados da venda solicitada.

    Lança:
    - HTTPException: Se a venda não for encontrada.
    """
    db_sales = get_sales_by_id(db, sales_id=sales_id)
    if db_sales is None:
        raise HTTPException(status_code=404, detail="Sales not found")
    return db_sales


@router.delete("/sales/{sales_id}", response_model=SalesResponse)
def detele_sales_route(sales_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma venda específica.

    Parâmetros:
    - sales_id (int): ID da venda a ser deletada.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - SalesResponse: Dados da venda deletada.

    Lança:
    - HTTPException: Se a venda não for encontrada.
    """
    db_sales = delete_sales(db, sales_id=sales_id)
    if db_sales is None:
        raise HTTPException(status_code=404, detail="Sales not found")
    return db_sales


@router.put("/sales/{sales_id}", response_model=SalesResponse)
def update_sales_route(
    sales_id: int, sales: SalesUpdate, db: Session = Depends(get_db)
):
    """
    Atualiza uma venda específica.

    Parâmetros:
    - sales_id (int): ID da venda a ser atualizada.
    - sales (SalesUpdate): Dados atualizados da venda.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - SalesResponse: Dados da venda atualizada.

    Lança:
    - HTTPException: Se a venda não for encontrada.
    """
    db_sales = update_sales(db, sales_id=sales_id, sales=sales)
    if db_sales is None:
        raise HTTPException(status_code=404, detail="Sales not found")
    return db_sales
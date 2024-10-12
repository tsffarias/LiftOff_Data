from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal, get_db
from models.supplier.supplier_schema import SupplierResponse, SupplierUpdate, SupplierCreate
from typing import List
from crud.supplier.crud import (
    create_supplier,
    get_suppliers,
    get_supplier,
    delete_supplier,
    update_supplier,
)

router = APIRouter()

@router.post("/suppliers/", response_model=SupplierResponse)
def create_supplier_route(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """
    Cria um novo fornecedor.

    Parâmetros:
    - supplier (SupplierCreate): Dados do fornecedor a ser criado.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - SupplierResponse: Dados do fornecedor criado.
    """
    return create_supplier(db=db, supplier=supplier)

@router.get("/suppliers/", response_model=List[SupplierResponse])
def read_all_suppliers_route(db: Session = Depends(get_db)):
    """
    Retorna todos os fornecedores.

    Parâmetros:
    - db (Session): Sessão do banco de dados.

    Retorna:
    - List[SupplierResponse]: Lista de todos os fornecedores.
    """
    suppliers = get_suppliers(db)
    return suppliers

@router.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
def read_supplier_route(supplier_id: int, db: Session = Depends(get_db)):
    """
    Retorna um fornecedor específico.

    Parâmetros:
    - supplier_id (int): ID do fornecedor a ser retornado.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - SupplierResponse: Dados do fornecedor solicitado.

    Lança:
    - HTTPException: Se o fornecedor não for encontrado.
    """
    db_supplier = get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

@router.delete("/suppliers/{supplier_id}", response_model=SupplierResponse)
def delete_supplier_route(supplier_id: int, db: Session = Depends(get_db)):
    """
    Deleta um fornecedor específico.

    Parâmetros:
    - supplier_id (int): ID do fornecedor a ser deletado.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - SupplierResponse: Dados do fornecedor deletado.

    Lança:
    - HTTPException: Se o fornecedor não for encontrado.
    """
    db_supplier = delete_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

@router.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
def update_supplier_route(
    supplier_id: int, supplier: SupplierUpdate, db: Session = Depends(get_db)
):
    """
    Atualiza um fornecedor específico.

    Parâmetros:
    - supplier_id (int): ID do fornecedor a ser atualizado.
    - supplier (SupplierUpdate): Dados atualizados do fornecedor.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - SupplierResponse: Dados do fornecedor atualizado.

    Lança:
    - HTTPException: Se o fornecedor não for encontrado.
    """
    db_supplier = update_supplier(db, supplier_id=supplier_id, supplier=supplier)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier



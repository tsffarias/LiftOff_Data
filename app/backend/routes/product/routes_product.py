from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from models.product.product_schema import ProductResponse, ProductUpdate, ProductCreate
from typing import List
from crud.product.crud import (
    create_product,
    get_products,
    get_product,
    delete_product,
    update_product,
)

router = APIRouter()

@router.post("/products/", response_model=ProductResponse)
async def create_product_route(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    """
    Cria um novo produto.

    Parâmetros:
    - product (ProductCreate): Dados do produto a ser criado.
    - db (AsyncSession): Sessão do banco de dados.

    Retorna:
    - ProductResponse: Dados do produto criado.
    """
    return await create_product(db=db, product=product)

@router.get("/products/", response_model=List[ProductResponse])
async def read_all_products_route(db: AsyncSession = Depends(get_db)):
    """
    Retorna todos os produtos.

    Parâmetros:
    - db (AsyncSession): Sessão do banco de dados.

    Retorna:
    - List[ProductResponse]: Lista de todos os produtos.
    """
    products = await get_products(db)
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
async def read_product_route(product_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retorna um produto específico.

    Parâmetros:
    - product_id (int): ID do produto a ser retornado.
    - db (AsyncSession): Sessão do banco de dados.

    Retorna:
    - ProductResponse: Dados do produto solicitado.

    Lança:
    - HTTPException: Se o produto não for encontrado.
    """
    db_product = await get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/products/{product_id}", response_model=ProductResponse)
async def delete_product_route(product_id: int, db: AsyncSession = Depends(get_db)):
    """
    Deleta um produto específico.

    Parâmetros:
    - product_id (int): ID do produto a ser deletado.
    - db (AsyncSession): Sessão do banco de dados.

    Retorna:
    - ProductResponse: Dados do produto deletado.

    Lança:
    - HTTPException: Se o produto não for encontrado.
    """
    db_product = await delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product_route(product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    """
    Atualiza um produto específico.

    Parâmetros:
    - product_id (int): ID do produto a ser atualizado.
    - product (ProductUpdate): Dados atualizados do produto.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - ProductResponse: Dados do produto atualizado.

    Lança:
    - HTTPException: Se o produto não for encontrado.
    """
    db_product = await update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
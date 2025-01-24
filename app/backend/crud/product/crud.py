from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.product.product_schema import ProductUpdate, ProductCreate
from models.product.product import ProductModel


async def get_product(db: AsyncSession, product_id: int):
    """
    Funcao que recebe um id e retorna somente ele
    """
    result = await db.execute(select(ProductModel).filter(ProductModel.id == product_id))
    return result.scalars().first()

async def get_products(db: AsyncSession):
    """
    Funcao que retorna todos os elementos
    """
    result = await db.execute(select(ProductModel))
    return result.scalars().all()

async def create_product(db: AsyncSession, product: ProductCreate):
    """
    Cria um novo produto.
    """
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def delete_product(db: AsyncSession, product_id: int):
    """
    Deleta um produto específico.
    """
    db_product = await get_product(db, product_id)
    if db_product:
        await db.delete(db_product)
        await db.commit()
    return db_product

async def update_product(db: AsyncSession, product_id: int, product: ProductUpdate):
    """
    Atualiza um produto existente.
    """
    db_product = await get_product(db, product_id)
    if db_product is None:
        return None

    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    await db.commit()
    await db.refresh(db_product)
    return db_product
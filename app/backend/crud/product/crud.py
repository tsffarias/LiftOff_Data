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
    Atualiza apenas os campos modificados de um produto.
    """
    db_product = await get_product(db, product_id)
    if db_product is None:
        return None

    # Obtém apenas os campos que foram alterados
    update_data = product.model_dump(exclude_unset=True)

    # Atualiza apenas os campos que realmente foram modificados
    for key, value in update_data.items():
        current_value = getattr(db_product, key, None)
        if current_value != value:  # Atualiza somente se o valor for diferente
            setattr(db_product, key, value)

    if update_data:  # Apenas realiza commit se houver alterações
        await db.commit()
        await db.refresh(db_product)

    return db_product

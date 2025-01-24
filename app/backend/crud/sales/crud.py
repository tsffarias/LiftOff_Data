from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.sales.sales_schema import SalesUpdate, SalesCreate
from models.sales.sales import SalesModel


async def get_sales_by_id(db: AsyncSession, sales_id: int):
    """
    Funcao que recebe um id e retorna somente ele
    """
    result = await db.execute(select(SalesModel).filter(SalesModel.id == sales_id))
    return result.scalars().first()

async def get_sales(db: AsyncSession):
    """
    Funcao que retorna todos os elementos
    """
    result = await db.execute(select(SalesModel))
    return result.scalars().all()

async def create_sales(db: AsyncSession, sales: SalesCreate):
    """
    Cria uma nova venda.
    """
    db_sales = SalesModel(**sales.model_dump())
    db.add(db_sales)
    await db.commit()
    await db.refresh(db_sales)
    return db_sales

async def delete_sales(db: AsyncSession, sales_id: int):
    """
    Deleta uma venda específica.
    """
    db_sales = await get_sales_by_id(db, sales_id)
    if db_sales:
        await db.delete(db_sales)
        await db.commit()
    return db_sales

async def update_sales(db: AsyncSession, sales_id: int, sales: SalesUpdate):
    """
    Atualiza uma venda existente.
    """
    db_sales = await get_sales_by_id(db, sales_id)
    if db_sales is None:
        return None

    update_data = sales.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sales, key, value)

    await db.commit()
    await db.refresh(db_sales)
    return db_sales
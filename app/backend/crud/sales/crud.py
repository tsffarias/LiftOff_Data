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
    Atualiza apenas os campos modificados de uma venda existente.
    """
    db_sales = await get_sales_by_id(db, sales_id)
    if db_sales is None:
        return None

    # Obtém apenas os campos que foram alterados
    update_data = sales.model_dump(exclude_unset=True)

    # Atualiza somente os campos que realmente foram modificados
    for key, value in update_data.items():
        current_value = getattr(db_sales, key, None)
        if current_value != value:  # Atualiza somente se o valor for diferente
            setattr(db_sales, key, value)

    if update_data:  # Realiza commit apenas se houver alterações
        await db.commit()
        await db.refresh(db_sales)

    return db_sales

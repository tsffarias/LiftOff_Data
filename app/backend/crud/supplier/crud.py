from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.supplier.supplier_schema import SupplierUpdate, SupplierCreate
from models.supplier.supplier import SupplierModel


async def get_supplier(db: AsyncSession, supplier_id: int):
    """
    Função que recebe um id e retorna somente o fornecedor correspondente
    """
    result = await db.execute(select(SupplierModel).filter(SupplierModel.supplier_id == supplier_id))
    return result.scalars().first()


async def get_suppliers(db: AsyncSession):
    """
    Função que retorna todos os fornecedores
    """
    result = await db.execute(select(SupplierModel))
    return result.scalars().all()

async def create_supplier(db: AsyncSession, supplier: SupplierCreate):
    """
    Cria um novo fornecedor.
    """
    db_supplier = SupplierModel(**supplier.model_dump())
    db.add(db_supplier)
    await db.commit()
    await db.refresh(db_supplier)
    return db_supplier

async def delete_supplier(db: AsyncSession, supplier_id: int):
    """
    Deleta um fornecedor específico.
    """
    db_supplier = await get_supplier(db, supplier_id)
    if db_supplier:
        await db.delete(db_supplier)
        await db.commit()
    return db_supplier

async def update_supplier(db: AsyncSession, supplier_id: int, supplier: SupplierUpdate):
    """
    Atualiza apenas os campos modificados de um fornecedor existente.
    """
    db_supplier = await get_supplier(db, supplier_id)
    if db_supplier is None:
        return None

    # Obtém apenas os campos que foram alterados
    update_data = supplier.model_dump(exclude_unset=True)

    # Atualiza somente os campos que realmente foram modificados
    for key, value in update_data.items():
        current_value = getattr(db_supplier, key, None)
        if current_value != value:  # Atualiza somente se o valor for diferente
            setattr(db_supplier, key, value)

    if update_data:  # Realiza commit apenas se houver alterações
        await db.commit()
        await db.refresh(db_supplier)

    return db_supplier



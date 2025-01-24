from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.employee.employee_schema import EmployeeUpdate, EmployeeCreate
from models.employee.employee import EmployeeModel

async def get_employee(db: AsyncSession, employee_id: int):
    """
    Função que recebe um id e retorna somente o funcionário correspondente
    """
    result = await db.execute(select(EmployeeModel).where(EmployeeModel.employee_id == employee_id))
    return result.scalars().first()

async def get_employees(db: AsyncSession):
    """
    Função que retorna todos os funcionários
    """
    result = await db.execute(select(EmployeeModel))
    return result.scalars().all()

async def create_employee(db: AsyncSession, employee: EmployeeCreate):
    """
    Função que cria um novo funcionário
    """
    db_employee = EmployeeModel(**employee.model_dump())
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee

async def delete_employee(db: AsyncSession, employee_id: int):
    """
    Função que deleta um funcionário
    """
    db_employee = await get_employee(db, employee_id=employee_id)
    if db_employee:
        await db.delete(db_employee)
        await db.commit()
    return db_employee

async def update_employee(db: AsyncSession, employee_id: int, employee: EmployeeUpdate):
    """
    Função que atualiza um funcionário
    """
    db_employee = await get_employee(db, employee_id=employee_id)
    if db_employee is None:
        return None

    update_data = employee.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)

    await db.commit()
    await db.refresh(db_employee)
    return db_employee

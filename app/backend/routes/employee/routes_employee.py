from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from models.employee.employee_schema import EmployeeResponse, EmployeeUpdate, EmployeeCreate
from typing import List
from crud.employee.crud import (
    create_employee,
    get_employees,
    get_employee,
    delete_employee,
    update_employee,
)

router = APIRouter()

@router.post("/employees/", response_model=EmployeeResponse)
async def create_employee_route(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    """
    Cria um novo funcionário.

    Parâmetros:
    - employee (EmployeeCreate): Dados do funcionário a ser criado.
    - db (AsyncSession): Sessão do banco de dados.

    Retorna:
    - EmployeeResponse: Dados do funcionário criado.

    Lança:
    - HTTPException: Se houver um problema ao criar o funcionário.
    """
    try:
        return await create_employee(db=db, employee=employee)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar funcionário: {str(e)}")


@router.get("/employees/", response_model=List[EmployeeResponse])
async def read_all_employees_route(db: AsyncSession = Depends(get_db)):
    """
    Retorna todos os funcionários.

    Parâmetros:
    - db (AsyncSession): Sessão do banco de dados.

    Retorna:
    - List[EmployeeResponse]: Lista de todos os funcionários.

    Lança:
    - HTTPException: Se não houver funcionários no banco de dados.
    """
    employees = await get_employees(db)
    if not employees:
        raise HTTPException(status_code=404, detail="Não há dados no banco de dados")
    return employees

@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def read_employee_route(employee_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retorna um funcionário específico.

    Parâmetros:
    - employee_id (int): ID do funcionário a ser retornado.
    - db (AsyncSession): Sessão do banco de dados.

    Retorna:
    - EmployeeResponse: Dados do funcionário solicitado.

    Lança:
    - HTTPException: Se o funcionário não for encontrado.
    """
    db_employee = await get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return db_employee

@router.delete("/employees/{employee_id}", response_model=EmployeeResponse)
async def delete_employee_route(employee_id: int, db: AsyncSession = Depends(get_db)):
    """
    Deleta um funcionário específico.

    Parâmetros:
    - employee_id (int): ID do funcionário a ser deletado.
    - db (AsyncSession): Sessão do banco de dados.

    Retorna:
    - EmployeeResponse: Dados do funcionário deletado.

    Lança:
    - HTTPException: Se o funcionário não for encontrado.
    """
    db_employee = await delete_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return db_employee

@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee_route(
    employee_id: int, employee: EmployeeUpdate, db: AsyncSession = Depends(get_db)):
    """
    Atualiza um funcionário específico.

    Parâmetros:
    - employee_id (int): ID do funcionário a ser atualizado.
    - employee (EmployeeUpdate): Dados atualizados do funcionário.
    - db (AsyncSession): Sessão do banco de dados.

    Retorna:
    - EmployeeResponse: Dados do funcionário atualizado.

    Lança:
    - HTTPException: Se o funcionário não for encontrado.
    """
    db_employee = await update_employee(db, employee_id=employee_id, employee=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return db_employee

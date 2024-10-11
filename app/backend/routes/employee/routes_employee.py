from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal, get_db
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
def create_employee_route(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """
    Cria um novo funcionário.

    Parâmetros:
    - employee (EmployeeCreate): Dados do funcionário a ser criado.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - EmployeeResponse: Dados do funcionário criado.
    """
    return create_employee(db=db, employee=employee)


@router.get("/employees/", response_model=List[EmployeeResponse])
def read_all_employees_route(db: Session = Depends(get_db)):
    """
    Retorna todos os funcionários.

    Parâmetros:
    - db (Session): Sessão do banco de dados.

    Retorna:
    - List[EmployeeResponse]: Lista de todos os funcionários.
    """
    employees = get_employees(db)
    return employees


@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
def read_employee_route(employee_id: int, db: Session = Depends(get_db)):
    """
    Retorna um funcionário específico.

    Parâmetros:
    - employee_id (int): ID do funcionário a ser retornado.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - EmployeeResponse: Dados do funcionário solicitado.

    Lança:
    - HTTPException: Se o funcionário não for encontrado.
    """
    db_employee = get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.delete("/employees/{employee_id}", response_model=EmployeeResponse)
def delete_employee_route(employee_id: int, db: Session = Depends(get_db)):
    """
    Deleta um funcionário específico.

    Parâmetros:
    - employee_id (int): ID do funcionário a ser deletado.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - EmployeeResponse: Dados do funcionário deletado.

    Lança:
    - HTTPException: Se o funcionário não for encontrado.
    """
    db_employee = delete_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee_route(
    employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)
):
    """
    Atualiza um funcionário específico.

    Parâmetros:
    - employee_id (int): ID do funcionário a ser atualizado.
    - employee (EmployeeUpdate): Dados atualizados do funcionário.
    - db (Session): Sessão do banco de dados.

    Retorna:
    - EmployeeResponse: Dados do funcionário atualizado.

    Lança:
    - HTTPException: Se o funcionário não for encontrado.
    """
    db_employee = update_employee(db, employee_id=employee_id, employee=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

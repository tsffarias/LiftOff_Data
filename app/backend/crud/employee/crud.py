from sqlalchemy.orm import Session
from models.employee.employee_schema import EmployeeUpdate, EmployeeCreate
from models.employee.employee import EmployeeModel


def get_employee(db: Session, employee_id: int):
    """
    Função que recebe um id e retorna somente o funcionário correspondente
    """
    return db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()


def get_employees(db: Session):
    """
    Função que retorna todos os funcionários
    """
    return db.query(EmployeeModel).all()


def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = EmployeeModel(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()
    db.delete(db_employee)
    db.commit()
    return db_employee


def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.employee_id == employee_id).first()

    if db_employee is None:
        return None

    update_data = employee.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee

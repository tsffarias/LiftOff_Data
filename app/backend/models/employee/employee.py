from sqlalchemy import Column, Integer, String, Float, Date, Enum as SQLAlchemyEnum, DateTime
from sqlalchemy.sql import func
from database.database import Base
from .employee_schema import GenderEnum


class EmployeeModel(Base):
    """
    Modelo de dados para representar um funcionário no banco de dados.

    Atributos:
        employee_id (Integer): Identificador único do funcionário, chave primária.
        first_name (String): Nome do funcionário.
        last_name (String): Sobrenome do funcionário.
        email (String): Endereço de email do funcionário.
        phone_number (String): Número de telefone do funcionário.
        hire_date (Date): Data de contratação do funcionário.
        department_id (Integer): Identificador do departamento.
        job_title (String): Cargo do funcionário.
        location (String): Localização do funcionário (cidade, estado, país).
        birth_date (Date): Data de nascimento do funcionário.
        gender (Enum): Gênero do funcionário.
        nationality (String): Nacionalidade do funcionário.
        start_date (Date): Data de início no cargo atual.
        salary (Float): Salário do funcionário.
        termination_date (Date): Data de término do contrato do funcionário, se aplicável.
        manager_id (Integer): Identificador do gerente, se aplicável.
    """

    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(Integer, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    hire_date = Column(Date, index=True)
    department_id = Column(Integer, index=True)
    job_title = Column(String)
    location = Column(String)
    birth_date = Column(Date)
    gender = Column(SQLAlchemyEnum(GenderEnum))
    nationality = Column(String)
    start_date = Column(Date)
    salary = Column(Float)
    termination_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)
from pydantic import BaseModel, EmailStr, PositiveFloat, field_validator, computed_field, validator
from enum import Enum
from datetime import date, datetime, timedelta
from typing import Optional


class GenderEnum(Enum):
    """
    Enum representando os gêneros dos funcionários.
    """
    male = "Masculino"
    female = "Feminino"
    prefer_not_to_say = "Prefiro não dizer"


class EmployeeBase(BaseModel):
    """
    Modelo base para informações do funcionário.

    Atributos:
        first_name (str): Nome do funcionário.
        last_name (str): Sobrenome do funcionário.
        email (EmailStr): Endereço de email do funcionário.
        phone_number (str): Número de telefone do funcionário.
        hire_date (date): Data de contratação do funcionário.
        department_id (int): Identificador do departamento.
        job_title (str): Cargo do funcionário.
        location (str): Localização do funcionário (cidade, estado, país).
        birth_date (date): Data de nascimento do funcionário.
        gender (GenderEnum): Gênero do funcionário.
        nationality (str): Nacionalidade do funcionário.
        start_date (date): Data de início no cargo atual.
        salary (PositiveFloat): Salário do funcionário.
        termination_date (Optional[date]): Data de término do contrato do funcionário, se aplicável.
    """
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    hire_date: date
    department_id: int
    manager_id: int
    job_title: str
    location: str
    birth_date: date
    gender: GenderEnum
    nationality: str
    start_date: date
    salary: PositiveFloat
    termination_date: Optional[date] = None


class EmployeeCreate(EmployeeBase):
    """
    Modelo para criar um novo funcionário. Herda todos os campos de EmployeeBase.
    """
    pass


class EmployeeResponse(EmployeeBase):
    """
    Modelo para resposta de funcionário, incluindo campos adicionais.

    Atributos:
        employee_id (int): O identificador único do funcionário.
        manager_id (Optional[int]): Identificador do gerente, se aplicável.
        service_duration (str): Duração do serviço do funcionário na empresa.
    """
    employee_id: int
    manager_id: Optional[int] = None

    @computed_field
    def service_duration(self) -> str:
        """
        Calcula a duração do serviço do funcionário até a data atual ou até a data de término.
        """
        end_date = self.termination_date or datetime.now().date()
        duration = end_date - self.hire_date
        years = duration.days // 365
        months = (duration.days % 365) // 30
        days = (duration.days % 365) % 30
        
        if years > 0:
            return f"{years} anos, {months} meses e {days} dias"
        elif months > 0:
            return f"{months} meses e {days} dias"
        else:
            return f"{days} dias"

    class Config:
        from_attributes = True


class EmployeeUpdate(BaseModel):
    """
    Modelo para atualizar um funcionário existente.

    Todos os campos são opcionais para permitir atualizações parciais.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    department_id: Optional[int] = None
    job_title: Optional[str] = None
    manager_id: Optional[int] = None
    location: Optional[str] = None
    gender: Optional[GenderEnum] = None
    nationality: Optional[str] = None
    start_date: Optional[date] = None
    salary: Optional[PositiveFloat] = None
    termination_date: Optional[date] = None

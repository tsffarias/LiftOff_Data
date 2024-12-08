from sqlalchemy.orm import Session
from models.sales.sales_schema import SalesUpdate, SalesCreate
from models.sales.sales import SalesModel


def get_sales_by_id(db: Session, sales_id: int):
    """
    funcao que recebe um id e retorna somente ele
    """
    return db.query(SalesModel).filter(SalesModel.id == sales_id).first()


def get_sales(db: Session):
    """
    funcao que retorna todos os elementos
    """
    return db.query(SalesModel).all()


def create_sales(db: Session, sales: SalesCreate):
    db_sales = SalesModel(**sales.model_dump())
    db.add(db_sales)
    db.commit()
    db.refresh(db_sales)
    return db_sales


def delete_sales(db: Session, sales_id: int):
    db_sales = db.query(SalesModel).filter(SalesModel.id == sales_id).first()
    db.delete(db_sales)
    db.commit()
    return db_sales


def update_sales(db: Session, sales_id: int, sales: SalesUpdate):
    db_sales = db.query(SalesModel).filter(SalesModel.id == sales_id).first()

    if db_sales is None:
        return None

    if sales.email_employee is not None:
        db_sales.email_employee = sales.email_employee
    if sales.email_customer is not None:
        db_sales.email_customer = sales.email_customer
    if sales.first_name is not None:
        db_sales.first_name = sales.first_name
    if sales.last_name is not None:
        db_sales.last_name = sales.last_name
    if sales.phone_number is not None:
        db_sales.phone_number = sales.phone_number
    if sales.price is not None:
        db_sales.price = sales.price
    if sales.quantity is not None:
        db_sales.quantity = sales.quantity
    if sales.name_product is not None:
        db_sales.name_product = sales.name_product
    if sales.date is not None:
        db_sales.date = sales.date    

    db.commit()
    return db_sales
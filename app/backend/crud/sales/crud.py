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

    if sales.email is not None:
        db_sales.email = sales.email
    if sales.valor is not None:
        db_sales.valor = sales.valor
    if sales.quantidade is not None:
        db_sales.quantidade = sales.quantidade
    if sales.produto is not None:
        db_sales.produto = sales.produto
    if sales.data is not None:
        db_sales.data = sales.data

    db.commit()
    return db_sales
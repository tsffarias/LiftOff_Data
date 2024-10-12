from sqlalchemy.orm import Session
from models.supplier.supplier_schema import SupplierUpdate, SupplierCreate
from models.supplier.supplier import SupplierModel


def get_supplier(db: Session, supplier_id: int):
    """
    Função que recebe um id e retorna somente o fornecedor correspondente
    """
    return db.query(SupplierModel).filter(SupplierModel.supplier_id == supplier_id).first()


def get_suppliers(db: Session):
    """
    Função que retorna todos os fornecedores
    """
    return db.query(SupplierModel).all()


def create_supplier(db: Session, supplier: SupplierCreate):
    """
    Função que cria um novo fornecedor
    """
    db_supplier = SupplierModel(**supplier.model_dump())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


def delete_supplier(db: Session, supplier_id: int):
    """
    Função que deleta um fornecedor
    """
    db_supplier = db.query(SupplierModel).filter(SupplierModel.supplier_id == supplier_id).first()
    db.delete(db_supplier)
    db.commit()
    return db_supplier


def update_supplier(db: Session, supplier_id: int, supplier: SupplierUpdate):
    """
    Função que atualiza um fornecedor
    """
    db_supplier = db.query(SupplierModel).filter(SupplierModel.supplier_id == supplier_id).first()

    if db_supplier is None:
        return None

    update_data = supplier.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_supplier, key, value)

    db.commit()
    db.refresh(db_supplier)
    return db_supplier


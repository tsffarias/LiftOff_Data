from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database.database import Base


class SalesModel(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    valor = Column(Float, index=True)
    quantidade = Column(Integer, index=True)
    produto = Column(String, index=True)
    data = Column(DateTime(timezone=True), index=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)
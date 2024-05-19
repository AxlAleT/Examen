from sqlalchemy import Column, Integer, CheckConstraint
from bd.base import Base

class Billete(Base):
    __tablename__ = "Billete"

    ID_Billete = Column(Integer, primary_key=True, nullable=False, unique=True)
    Denominacion = Column(Integer, CheckConstraint('Denominacion >= 20 AND Denominacion <= 1000'), nullable=False )
    Cantidad = Column(Integer)
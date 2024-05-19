from sqlalchemy import Column, Integer, String
from bd.base import Base

class Billete(Base):
    __tablename__ = "Billete"

    ID_Billete = Column(Integer, primary_key=True)
    Denominacion = Column(Integer)
    Cantidad = Column(Integer)
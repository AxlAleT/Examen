from sqlalchemy import Column, Integer, String
from bd.base import Base

class Servicio(Base):
    __tablename__ = "Servicio"

    Num_Convenio = Column(Integer, primary_key=True, nullable=False, unique=True)
    NombreServicio = Column(String(100), nullable=False)
    Descripcion = Column(String(100))
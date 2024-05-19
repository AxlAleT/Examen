from sqlalchemy import Column, Integer, String
from bd.base import Base

class Servicio(Base):
    __tablename__ = "Servicio"

    Num_Convenio = Column(Integer, primary_key=True)
    NombreServicio = Column(String(100))
    Descripcion = Column(String(100))
from sqlalchemy import Column, Integer, String
from bd.base import Base

class Servicio(Base):
    """
    Clase que representa un servicio en la base de datos.

    Attributes:
        Num_Convenio (int): Número de convenio del servicio (clave primaria).
        NombreServicio (str): Nombre del servicio.
        Descripcion (str): Descripción del servicio.
    """
    __tablename__ = "Servicio"

    Num_Convenio = Column(Integer, primary_key=True, nullable=False, unique=True)
    NombreServicio = Column(String(100), nullable=False)
    Descripcion = Column(String(100))

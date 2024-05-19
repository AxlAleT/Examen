from sqlalchemy import Column, Integer, String
from bd.base import Base

class Cuenta(Base):
    __tablename__ = "Cuenta"

    Num_Cuenta = Column(Integer, primary_key=True, nullable=False, unique=True)
    CuentaHabiente = Column(String(50), nullable=False, unique=True)
    Direccion = Column(String(300), nullable=False)

    def __str__(self):
        return self.CuentaHabiente

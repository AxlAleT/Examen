from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from modelos.Cuenta import Cuenta
from modelos.Movimiento import Movimiento
from bd.base import Base

class Cuenta_Movimiento(Base):
    __tablename__ = "Cuenta_Movimiento"

    ID_Cuenta_Movimiento = Column(Integer, primary_key = True)

    Num_Cuenta = Column(Integer, ForeignKey("Cuenta.Num_Cuenta") )
    Cuenta = relationship(Cuenta)

    ID_Movimiento = Column(Integer, ForeignKey("Movimiento.ID_Movimiento"))
    Movimiento = relationship(Movimiento)
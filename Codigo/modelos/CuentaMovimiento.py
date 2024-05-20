from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from modelos.Cuenta import Cuenta
from modelos.Movimiento import Movimiento
from bd.base import Base

class Cuenta_Movimiento(Base):
    """
    Clase que representa la relación entre una cuenta y un movimiento en la base de datos.

    Attributes:
        ID_Cuenta_Movimiento (int): Identificador único de la relación.
        Num_Cuenta (int): Número de cuenta relacionado.
        Cuenta (Cuenta): Objeto de cuenta relacionado.
        ID_Movimiento (int): Identificador del movimiento relacionado.
        Movimiento (Movimiento): Objeto de movimiento relacionado.
    """
    __tablename__ = "Cuenta_Movimiento"

    ID_Cuenta_Movimiento = Column(Integer, primary_key=True, nullable=False, unique=True)

    Num_Cuenta = Column(Integer, ForeignKey("Cuenta.Num_Cuenta"), nullable=False )
    Cuenta = relationship(Cuenta)

    ID_Movimiento = Column(Integer, ForeignKey("Movimiento.ID_Movimiento"), nullable=False)
    Movimiento = relationship(Movimiento)

from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from modelos.Cuenta import Cuenta
from bd.base import Base

class Tarjeta_Debito(Base):
    __tablename__ = "Tarjeta_Debito"

    NumeroTarjeta = Column(Integer, primary_key=True)
    Saldo = Column(DECIMAL)
    NIP = Column(Integer)
    Num_Cuenta = Column(Integer, ForeignKey("Cuenta.Num_Cuenta") )
    Cuenta = relationship(Cuenta)

    def __str__(self):
        return self.NumeroTarjeta
    
class Tarjeta_Credito(Base):
    __tablename__ = "Tarjeta_Credito"

    NumeroTarjeta = Column(Integer, primary_key=True)
    Saldo = Column(DECIMAL)
    LimiteCredito = Column(DECIMAL)
    NIP = Column(Integer)
    Num_Cuenta = Column(Integer, ForeignKey("Cuenta.Num_Cuenta") )
    Cuenta = relationship(Cuenta)

    def __str__(self):
        return self.NumeroTarjeta
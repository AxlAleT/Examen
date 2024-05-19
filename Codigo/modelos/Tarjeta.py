from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, String
from sqlalchemy.orm import relationship
from modelos.Cuenta import Cuenta
from bd.base import Base
import bcrypt

class Tarjeta_Debito(Base):
    __tablename__ = "Tarjeta_Debito"

    NumeroTarjeta = Column(Integer, primary_key=True, nullable=False, unique=True)
    Saldo = Column(DECIMAL)
    nip_hash = Column(String(60), nullable=False)
    Num_Cuenta = Column(Integer, ForeignKey("Cuenta.Num_Cuenta"), nullable=False, unique=True)
    Cuenta = relationship(Cuenta)

    def __str__(self):
        return self.NumeroTarjeta
    
    def set_nip(self, nip):
        # Generar un hash para el NIP
        self.nip_hash = bcrypt.hashpw(nip.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_nip(self, nip):
        # Verificar si el NIP coincide con el hash almacenado
        return bcrypt.checkpw(nip.encode('utf-8'), self.nip_hash.encode('utf-8'))
    
class Tarjeta_Credito(Base):
    __tablename__ = "Tarjeta_Credito"

    NumeroTarjeta = Column(Integer, primary_key=True, nullable=False, unique=True)
    Saldo = Column(DECIMAL)
    LimiteCredito = Column(DECIMAL)
    nip_hash = Column(String(60), nullable=False)
    Num_Cuenta = Column(Integer, ForeignKey("Cuenta.Num_Cuenta"), nullable=False, unique=True)
    Cuenta = relationship(Cuenta)

    def __str__(self):
        return self.NumeroTarjeta
    
    def set_nip(self, nip):
        # Generar un hash para el NIP
        self.nip_hash = bcrypt.hashpw(nip.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_nip(self, nip):
        # Verificar si el NIP coincide con el hash almacenado
        return bcrypt.checkpw(nip.encode('utf-8'), self.nip_hash.encode('utf-8'))
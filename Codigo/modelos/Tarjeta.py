from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, String
from sqlalchemy.orm import relationship
from modelos.Cuenta import Cuenta
from bd.base import Base
from excepciones import excepciones_tarjeta
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
    
    @classmethod
    def obtener_tarjeta_Debito_numero(cls,numero_tarjeta, sesion):
        return sesion.query(Tarjeta_Debito).filter_by(NumeroTarjeta=numero_tarjeta).first()
    
    @staticmethod
    def validar_Tarjeta(num_tarjeta):
        
        # Convertir el entero a cadena para verificar la longitud y el prefijo
        tarjeta_str = str(num_tarjeta)
        
        # Verificar si la cadena tiene exactamente 16 dígitos y comienza con "400000"
        if len(tarjeta_str) == 16 and tarjeta_str.isdigit() and tarjeta_str.startswith("400000"):
            return True
        else:
            return False
    
    @classmethod
    def validar_y_obtener_tarjeta(cls, num_tarjeta, nip, sesion):
        if cls.validar_Tarjeta(num_tarjeta):
            tarjeta_credito = cls.obtener_tarjeta_Debito_numero(num_tarjeta, sesion)
            if tarjeta_credito is None:
                raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de crédito incorrecto")
            if not tarjeta_credito.check_nip(nip):  
                raise excepciones_tarjeta.NipIncorrecto("NIP incorrecto")
            return tarjeta_credito
        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de crédito incorrecto")


    

    
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
    
    @classmethod
    def obtener_tarjeta_Credito_numero(cls,numero_tarjeta, sesion):
        return sesion.query(Tarjeta_Credito).filter_by(NumeroTarjeta=numero_tarjeta).first()
    
    @staticmethod
    def validar_Tarjeta(num_tarjeta):
       
        # Convertir el entero a cadena para verificar la longitud y el prefijo
        tarjeta_str = str(num_tarjeta)
        
        # Verificar si la cadena tiene exactamente 16 dígitos y comienza con "400000"
        if len(tarjeta_str) == 16 and tarjeta_str.isdigit() and tarjeta_str.startswith("500000"):
            return True
        else:
            return False
        
    @classmethod
    def validar_y_obtener_tarjeta(cls, num_tarjeta, nip, sesion):
        if cls.validar_Tarjeta(num_tarjeta):
            tarjeta_credito = cls.obtener_tarjeta_Debito_numero(num_tarjeta, sesion)
            if tarjeta_credito is None:
                raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de crédito incorrecto")
            if not tarjeta_credito.check_nip(nip):  
                raise excepciones_tarjeta.NipIncorrecto("NIP incorrecto")
            return tarjeta_credito
        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de crédito incorrecto")

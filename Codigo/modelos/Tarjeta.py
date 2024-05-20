from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, String
from sqlalchemy.orm import relationship
from modelos.Cuenta import Cuenta
from bd.base import Base
from excepciones import excepciones_tarjeta
import bcrypt

class Tarjeta_Debito(Base):
        """
    Clase que representa una tarjeta de débito en la base de datos.

    Attributes:
        NumeroTarjeta (int): Número de tarjeta de débito (clave primaria).
        Saldo (DECIMAL): Saldo de la tarjeta de débito.
        nip_hash (str): Hash del NIP de la tarjeta de débito.
        Num_Cuenta (int): Número de cuenta asociado a la tarjeta de débito (clave foránea).
        Cuenta (Cuenta): Relación con el objeto Cuenta.
    """
    __tablename__ = "Tarjeta_Debito"

    NumeroTarjeta = Column(Integer, primary_key=True, nullable=False, unique=True)
    Saldo = Column(DECIMAL)
    nip_hash = Column(String(60), nullable=False)
    Num_Cuenta = Column(Integer, ForeignKey("Cuenta.Num_Cuenta"), nullable=False, unique=True)
    Cuenta = relationship(Cuenta)

    def __str__(self):
        return self.NumeroTarjeta
    
    def set_nip(self, nip):
           """
        Establece el NIP de la tarjeta de débito.

        Args:
            nip (str): NIP a establecer.

        Returns:
            None
        """
        # Generar un hash para el NIP
        self.nip_hash = bcrypt.hashpw(nip.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_nip(self, nip):
          """
        Verifica si el NIP dado coincide con el NIP de la tarjeta.

        Args:
            nip (str): NIP a verificar.

        Returns:
            bool: True si el NIP coincide, False de lo contrario.
        """
        # Verificar si el NIP coincide con el hash almacenado
        return bcrypt.checkpw(nip.encode('utf-8'), self.nip_hash.encode('utf-8'))
    
    @classmethod
    def obtener_tarjeta_Debito_numero(cls,numero_tarjeta, sesion):
         """
        Obtiene una tarjeta de débito por su número.

        Args:
            numero_tarjeta (int): Número de tarjeta de débito a buscar.
            sesion: Sesión de base de datos.

        Returns:
            Tarjeta_Debito: Objeto de la tarjeta de débito si se encuentra, None de lo contrario.
        """
        return sesion.query(Tarjeta_Debito).filter_by(NumeroTarjeta=numero_tarjeta).first()
    
    @staticmethod
    def validar_Tarjeta(num_tarjeta):
            """
        Valida un número de tarjeta de débito.

        Args:
            num_tarjeta (int): Número de tarjeta de débito a validar.

        Returns:
            bool: True si el número de tarjeta es válido, False de lo contrario.
        """
        
        # Convertir el entero a cadena para verificar la longitud y el prefijo
        tarjeta_str = str(num_tarjeta)
        
        # Verificar si la cadena tiene exactamente 16 dígitos y comienza con "400000"
        if len(tarjeta_str) == 16 and tarjeta_str.isdigit() and tarjeta_str.startswith("400000"):
            return True
        else:
            return False
    
    @classmethod
    def validar_y_obtener_tarjeta(cls, num_tarjeta, nip, sesion):
          """
        Valida y obtiene una tarjeta de débito por su número y NIP.

        Args:
            num_tarjeta (int): Número de tarjeta de débito a validar y obtener.
            nip (str): NIP de la tarjeta de débito.
            sesion: Sesión de base de datos.

        Returns:
            Tarjeta_Debito: Objeto de la tarjeta de débito si es válido, None de lo contrario.

        Raises:
            NumeroTarjetaIncorrecto: Si el número de tarjeta no es válido.
            NipIncorrecto: Si el NIP no es correcto.
        """
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
     """
    Clase que representa una tarjeta de crédito en la base de datos.

    Attributes:
        NumeroTarjeta (int): Número de tarjeta de crédito (clave primaria).
        Saldo (DECIMAL): Saldo de la tarjeta de crédito.
        LimiteCredito (DECIMAL): Límite de crédito de la tarjeta de crédito.
        nip_hash (str): Hash del NIP de la tarjeta de crédito.
        Num_Cuenta (int): Número de cuenta asociado a la tarjeta de crédito (clave foránea).
        Cuenta (Cuenta): Relación con el objeto Cuenta.
    """
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
           """
        Establece el NIP de la tarjeta de crédito.

        Args:
            nip (str): NIP a establecer.

        Returns:
            None
        """
        # Generar un hash para el NIP
        self.nip_hash = bcrypt.hashpw(nip.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_nip(self, nip):
           """
        Verifica si el NIP dado coincide con el NIP de la tarjeta.

        Args:
            nip (str): NIP a verificar.

        Returns:
            bool: True si el NIP coincide, False de lo contrario.
        """
        # Verificar si el NIP coincide con el hash almacenado
        return bcrypt.checkpw(nip.encode('utf-8'), self.nip_hash.encode('utf-8'))
    
    @classmethod
    def obtener_tarjeta_Credito_numero(cls,numero_tarjeta, sesion):
           """
        Obtiene una tarjeta de crédito por su número.

        Args:
            numero_tarjeta (int): Número de tarjeta de crédito a buscar.
            sesion: Sesión de base de datos.

        Returns:
            Tarjeta_Credito: Objeto de la tarjeta de crédito si se encuentra, None de lo contrario.
        """
        return sesion.query(Tarjeta_Credito).filter_by(NumeroTarjeta=numero_tarjeta).first()
    
    @staticmethod
    def validar_Tarjeta(num_tarjeta):
          """
        Valida un número de tarjeta de crédito.

        Args:
            num_tarjeta (int): Número de tarjeta de crédito a validar.

        Returns:
            bool: True si el número de tarjeta es válido, False de lo contrario.
        """
       
        # Convertir el entero a cadena para verificar la longitud y el prefijo
        tarjeta_str = str(num_tarjeta)
        
        # Verificar si la cadena tiene exactamente 16 dígitos y comienza con "400000"
        if len(tarjeta_str) == 16 and tarjeta_str.isdigit() and tarjeta_str.startswith("500000"):
            return True
        else:
            return False
        
    @classmethod
    def validar_y_obtener_tarjeta(cls, num_tarjeta, nip, sesion):
           """
        Valida y obtiene una tarjeta de crédito por su número y NIP.

        Args:
            num_tarjeta (int): Número de tarjeta de crédito a validar y obtener.
            nip (str): NIP de la tarjeta de crédito.
            sesion: Sesión de base de datos.

        Returns:
            Tarjeta_Credito: Objeto de la tarjeta de crédito si es válido, None de lo contrario.

        Raises:
            NumeroTarjetaIncorrecto: Si el número de tarjeta no es válido.
            NipIncorrecto: Si el NIP no es correcto.
        """
        if cls.validar_Tarjeta(num_tarjeta):
            tarjeta_credito = cls.obtener_tarjeta_Debito_numero(num_tarjeta, sesion)
            if tarjeta_credito is None:
                raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de crédito incorrecto")
            if not tarjeta_credito.check_nip(nip):  
                raise excepciones_tarjeta.NipIncorrecto("NIP incorrecto")
            return tarjeta_credito
        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de crédito incorrecto")

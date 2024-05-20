from sqlalchemy import Column, Integer, String
from bd.base import Base

class Cuenta(Base):
    """
    Clase que representa una cuenta en la base de datos.

    Attributes:
        Num_Cuenta (int): Número único de la cuenta.
        CuentaHabiente (str): Nombre del titular de la cuenta.
        Direccion (str): Dirección asociada a la cuenta.
    """
    __tablename__ = "Cuenta"

    Num_Cuenta = Column(Integer, primary_key=True, nullable=False, unique=True)
    CuentaHabiente = Column(String(50), nullable=False, unique=True)
    Direccion = Column(String(300), nullable=False)

    def __str__(self):
        """
        Método para obtener una representación de cadena de la cuenta.

        Returns:
            str: Nombre del titular de la cuenta.
        """
        return self.CuentaHabiente

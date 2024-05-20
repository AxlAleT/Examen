from sqlalchemy import Column, Integer, Date, DECIMAL, String, ForeignKey
from bd.base import Base
from sqlalchemy.orm import relationship
from modelos.Servicio import Servicio


class Tipo_Movimiento(Base):
        """
    Clase que representa los tipos de movimiento en la base de datos.

    Attributes:
        ID_Tipo_Movimiento (int): Identificador único del tipo de movimiento.
        Tipo (str): Tipo de movimiento.
        Descripcion (str): Descripción del tipo de movimiento.
    """
    __tablename__ = "Tipo_Movimiento"
    ID_Tipo_Movimiento = Column(Integer, primary_key=True, nullable=False, unique=True)
    Tipo = Column(String(20), nullable=False)
    Descripcion = Column(String(100))


class Movimiento(Base):
        """
    Clase que representa un movimiento financiero en la base de datos.

    Attributes:
        ID_Movimiento (int): Identificador único del movimiento.
        Fecha (Date): Fecha del movimiento.
        Monto (DECIMAL): Monto del movimiento.
        ID_Tipo_Movimiento (int): Identificador del tipo de movimiento asociado.
        Tipo_Movimiento (Tipo_Movimiento): Objeto de tipo de movimiento asociado.
    """
    __tablename__ = "Movimiento"

    ID_Movimiento = Column(Integer, primary_key=True, nullable=False, unique=True)
    Fecha = Column(Date)
    Monto = Column(DECIMAL, nullable=False)
    ID_Tipo_Movimiento = Column(Integer, ForeignKey("Tipo_Movimiento.ID_Tipo_Movimiento"), nullable=False)
    Tipo_Movimiento = relationship(Tipo_Movimiento)

    def __str__(self):
             """
        Método para obtener una representación de cadena del movimiento.

        Returns:
            str: Representación de cadena del movimiento.
        """
        return f"Movimiento(ID_Movimiento={self.ID_Movimiento}, Fecha={self.Fecha}, Monto={self.Monto})"


class MovimientoPagoServicio(Base):
     """
    Clase que representa un movimiento de pago de servicio en la base de datos.

    Attributes:
        ID_Movimiento (int): Identificador del movimiento asociado.
        Movimiento (Movimiento): Objeto de movimiento asociado.
        Num_Convenio (int): Número de convenio del servicio asociado.
        Servicio (Servicio): Objeto de servicio asociado.
        Referencia (str): Referencia del pago de servicio.
    """
    __tablename__ = "Movimiento_pago_servicio"

    ID_Movimiento = Column(Integer, ForeignKey('Movimiento.ID_Movimiento'), primary_key=True, nullable=False)
    Movimiento = relationship(Movimiento)
    Num_Convenio = Column(ForeignKey("Servicio.Num_Convenio"), nullable=False)
    Servicio = relationship(Servicio)

    Referencia = Column(String)

    def __str__(self):
            """
        Método para obtener una representación de cadena del movimiento de pago de servicio.

        Returns:
            str: Representación de cadena del movimiento de pago de servicio.
        """
        return f"MovimientoPagoServicio(ID_Movimiento={self.ID_Movimiento}, NumeroConvenio={self.NumeroConvenio}, Referencia={self.Referencia})"

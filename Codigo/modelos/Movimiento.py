from sqlalchemy import Column, Integer, Date, DECIMAL, String, ForeignKey
from bd.base import Base
from sqlalchemy.orm import relationship
from modelos.Servicio import Servicio


class Tipo_Movimiento(Base):
    __tablename__ = "Tipo_Movimiento"
    ID_Tipo_Movimiento = Column(Integer, primary_key=True)
    Tipo = Column(String(20))
    Descripcion = Column(String(100))


class Movimiento(Base):
    __tablename__ = "Movimiento"

    ID_Movimiento = Column(Integer, primary_key=True)
    Fecha = Column(Date)
    Monto = Column(DECIMAL)
    ID_Tipo_Movimiento = Column(Integer, ForeignKey("Tipo_Movimiento.ID_Tipo_Movimiento"))
    Tipo_Movimiento = relationship(Tipo_Movimiento)

    def __str__(self):
        return f"Movimiento(ID_Movimiento={self.ID_Movimiento}, Fecha={self.Fecha}, Monto={self.Monto})"


class MovimientoPagoServicio(Base):
    __tablename__ = "Movimiento_pago_servicio"

    ID_Movimiento = Column(Integer, ForeignKey('Movimiento.ID_Movimiento'), primary_key=True)
    Movimiento = relationship(Movimiento)
    Num_Convenio = Column(ForeignKey("Servicio.Num_Convenio"))
    Servicio = relationship(Servicio)

    Referencia = Column(String)

    def __str__(self):
        return f"MovimientoPagoServicio(ID_Movimiento={self.ID_Movimiento}, NumeroConvenio={self.NumeroConvenio}, Referencia={self.Referencia})"
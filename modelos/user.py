from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Definir la clase del modelo User (suponiendo que ya tienes este modelo definido)
class Cuenta(Base):
    __tablename__ = 'cuentas'

    id_cuenta = Column(Integer, primary_key=True)
    titular = Column(String)
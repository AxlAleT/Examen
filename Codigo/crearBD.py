from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bd.base import Base
from modelos import Billete
from modelos import Cuenta
from modelos import CuentaMovimiento
from modelos import Tarjeta
from modelos import Movimiento
from modelos import Tarjeta
from poblarBD import poblar

if __name__ == "__main__":
    engine = create_engine("sqlite:///Codigo/bd/base.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    poblar(engine=engine)

from modelos.Tarjeta import Tarjeta_Credito
from modelos.Tarjeta import Tarjeta_Debito
from sqlalchemy.orm import sessionmaker
from main import engine

class retiro_controlador(): 
    
    Session = sessionmaker(bind=engine)
    sesion = Session()

    
        
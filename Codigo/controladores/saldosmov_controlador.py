from sqlalchemy.orm import sessionmaker
from excepciones import excepciones_tarjeta
from modelos.Tarjeta import Tarjeta_Debito, Tarjeta_Credito
from bd.db_controlador import engine, sesion
from controladores.tarjeta_controlador import TarjetaControlador

class ConsultaControlador:
    # Inicialización de la sesión para interactuar con la base de datos
    Session = sessionmaker(bind=engine)
    sesion = Session()

    @staticmethod
    def consultar_saldo(num_tarjeta):
        # Método para consultar el saldo de una tarjeta de débito o crédito
        tarjeta = TarjetaControlador.obtener_tarjeta(num_tarjeta)
        return tarjeta.Saldo

  

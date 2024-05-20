from sqlalchemy.orm import sessionmaker
from excepciones import excepciones_tarjeta
from modelos.Account import Account
from modelos.Movement import Movement
from bd.db_controlador import engine, sesion

class ConsultaControlador:
    # Inicialización de la sesión para interactuar con la base de datos
    Session = sessionmaker(bind=engine)
    sesion = Session()

    @staticmethod
    def consultar_saldo(num_cuenta):
        # Método para consultar el saldo de una cuenta específica
        cuenta = ConsultaControlador.sesion.query(Account).filter_by(account_number=num_cuenta).first()
        if cuenta is None:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de cuenta incorrecto")
        return cuenta.balance

    @staticmethod
    def consultar_movimientos(num_cuenta):
        # Método para consultar los movimientos de una cuenta específica
        cuenta = ConsultaControlador.sesion.query(Account).filter_by(account_number=num_cuenta).first()
        if cuenta is None:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de cuenta incorrecto")
        return cuenta.movements

class ConsultaVista:
    # Clase para mostrar los datos al usuario
    @staticmethod
    def mostrar_saldo(saldo):
        # Método para mostrar el saldo actual
        print(f"Saldo Actual: ${saldo:.2f}")

    @staticmethod
    def mostrar_movimientos(movimientos):
        # Método para mostrar los movimientos de la cuenta
        print("Movimientos:")
        for movimiento in movimientos:
            print(f"  {movimiento.description}: ${movimiento.amount:.2f}")

if __name__ == "__main__":
    controlador = ConsultaControlador()

    
    num_cuenta = "1234"  

    try:
        # Consulta del saldo y los movimientos de la cuenta
        saldo = controlador.consultar_saldo(num_cuenta)
        ConsultaVista.mostrar_saldo(saldo)
        
        movimientos = controlador.consultar_movimientos(num_cuenta)
        ConsultaVista.mostrar_movimientos(movimientos)
    except excepciones_tarjeta.NumeroTarjetaIncorrecto as e:
        # Manejo de errores si el número de cuenta es incorrecto
        print(e)

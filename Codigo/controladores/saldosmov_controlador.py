from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from excepciones import excepciones_tarjeta
from modelos.Cuenta import Cuenta
from modelos.Movimiento import Movimiento
from modelos.Tarjeta import Tarjeta_Debito, Tarjeta_Credito
from bd.db_controlador import engine

class ConsultaControlador:
    # Inicialización de la sesión para interactuar con la base de datos
    Session = sessionmaker(bind=engine)
    sesion = Session()

    @staticmethod
    def consultar_saldo(num_tarjeta):
        # Método para consultar el saldo de una cuenta específica a través del número de tarjeta
        tarjeta_debito = ConsultaControlador.sesion.query(Tarjeta_Debito).filter_by(NumeroTarjeta=num_tarjeta).first()
        tarjeta_credito = ConsultaControlador.sesion.query(Tarjeta_Credito).filter_by(NumeroTarjeta=num_tarjeta).first()

        if tarjeta_debito:
            return float(tarjeta_debito.Saldo)
        elif tarjeta_credito:
            return float(tarjeta_credito.Saldo)
        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")

    @staticmethod
    def consultar_movimientos(num_tarjeta):
        # Método para consultar los movimientos de una cuenta específica a través del número de tarjeta
        tarjeta_debito = ConsultaControlador.sesion.query(Tarjeta_Debito).filter_by(NumeroTarjeta=num_tarjeta).first()
        tarjeta_credito = ConsultaControlador.sesion.query(Tarjeta_Credito).filter_by(NumeroTarjeta=num_tarjeta).first()
        
        cuenta_numero = None

        if tarjeta_debito:
            cuenta_numero = tarjeta_debito.Num_Cuenta
        elif tarjeta_credito:
            cuenta_numero = tarjeta_credito.Num_Cuenta
        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")

        movimientos = ConsultaControlador.sesion.query(Movimiento).join(Cuenta_Movimiento).filter(Cuenta_Movimiento.Num_Cuenta == cuenta_numero).all()
        
        return [(movimiento.Monto, movimiento.Fecha, movimiento.Tipo_Movimiento.Tipo) for movimiento in movimientos]

from modelos.Tarjeta import Tarjeta_Credito, Tarjeta_Debito
from sqlalchemy.orm import sessionmaker
from main import engine
from excepciones.excepciones_tarjeta import NumeroTarjetaIncorrecto, NipIncorrecto, SaldoInsuficiente
from excepciones.excepciones_billete import NoSePuedeDarMontoException
from modelos.Billete import Billete
from modelos.CuentaMovimiento import Cuenta_Movimiento
from modelos.Movimiento import Movimiento, Tipo_Movimiento
from datetime import datetime

class DepositoControlador(): 
    
    Session = sessionmaker(bind=engine)
    sesion = Session()

    @staticmethod
    def depositar(num_tarjeta, monto, nip):
        # Verificar si es una tarjeta de crédito válida
        if Tarjeta_Credito.validar_Tarjeta(num_tarjeta):
            tarjeta_credito = Tarjeta_Credito.obtener_tarjeta_Credito_numero(num_tarjeta, DepositoControlador.sesion)
            if tarjeta_credito is None:
                raise NumeroTarjetaIncorrecto("Número de tarjeta de crédito incorrecto")
            if not tarjeta_credito.check_nip(nip):
                raise NipIncorrecto("NIP incorrecto")

            # Realizar el depósito
            tarjeta_credito.Saldo += monto

            # Crear el movimiento de depósito
            tipo_deposito = DepositoControlador.sesion.query(Tipo_Movimiento).filter_by(Tipo='Depósito de efectivo').first()
            movimiento = Movimiento(
                Fecha=datetime.now(),
                Monto=monto,
                ID_Tipo_Movimiento=tipo_deposito.ID_Tipo_Movimiento
            )
            DepositoControlador.sesion.add(movimiento)

            # Relacionar el movimiento con la cuenta
            cuenta_movimiento = Cuenta_Movimiento(
                Num_Cuenta=tarjeta_credito.Num_Cuenta,
                Movimiento=movimiento
            )
            DepositoControlador.sesion.add(cuenta_movimiento)

            DepositoControlador.sesion.commit()
            return True
        
        # Verificar si es una tarjeta de débito válida
        elif Tarjeta_Debito.validar_Tarjeta(num_tarjeta):
            tarjeta_debito = Tarjeta_Debito.obtener_tarjeta_Debito_numero(num_tarjeta, DepositoControlador.sesion)
            if tarjeta_debito is None:
                raise NumeroTarjetaIncorrecto("Número de tarjeta de débito incorrecto")
            if not tarjeta_debito.check_nip(nip):
                raise NipIncorrecto("NIP incorrecto")

            # Realizar el depósito
            tarjeta_debito.Saldo += monto

            # Crear el movimiento de depósito
            tipo_deposito = DepositoControlador.sesion.query(Tipo_Movimiento).filter_by(Tipo='Depósito de efectivo').first()
            movimiento = Movimiento(
                Fecha=datetime.now(),
                Monto=monto,
                ID_Tipo_Movimiento=tipo_deposito.ID_Tipo_Movimiento
            )
            DepositoControlador.sesion.add(movimiento)

            # Relacionar el movimiento con la cuenta
            cuenta_movimiento = Cuenta_Movimiento(
                Num_Cuenta=tarjeta_debito.Num_Cuenta,
                Movimiento=movimiento
            )
            DepositoControlador.sesion.add(cuenta_movimiento)

            DepositoControlador.sesion.commit()
            return True
        
        else:
            raise NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")

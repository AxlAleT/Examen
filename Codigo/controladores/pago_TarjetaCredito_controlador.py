from modelos.Tarjeta import Tarjeta_Credito, Tarjeta_Debito
from sqlalchemy.orm import sessionmaker
from bd.db_controlador import engine
from excepciones.excepciones_tarjeta import NumeroTarjetaIncorrecto
from excepciones.excepciones_billete import NoSePuedeDarMontoException, DenominacionNoExistente
from modelos.Billete import Billete
from modelos.CuentaMovimiento import Cuenta_Movimiento
from modelos.Movimiento import Movimiento, Tipo_Movimiento
from datetime import datetime

class PagoTarjetaCreditoControlador():
    Session = sessionmaker(bind=engine)
    sesion = Session()

    @staticmethod
    def pagar_tarjeta_credito(num_tarjeta, monto):
        # Convertir el monto a float para asegurarse de que se maneja correctamente
        try:
            monto = float(monto)
        except ValueError:
            raise ValueError("Monto debe ser un número válido")

        # Obtener las denominaciones de billetes disponibles en orden descendente
        denominaciones = PagoTarjetaCreditoControlador.sesion.query(Billete).order_by(Billete.Denominacion.desc()).all()

        # Actualizar la cantidad de billetes en la base de datos
        monto_restante = monto
        for billete in denominaciones:
            cantidad_a_introducir = int(monto_restante // billete.Denominacion)
            if cantidad_a_introducir > 0:
                try:
                    Billete.agregar_billete(billete.Denominacion, cantidad_a_introducir, PagoTarjetaCreditoControlador.sesion)
                    monto_restante -= cantidad_a_introducir * billete.Denominacion
                except DenominacionNoExistente as e:
                    raise NoSePuedeDarMontoException(f"Error al procesar billetes: {str(e)}")

        # Verificar si es una tarjeta de crédito válida
        tarjeta_credito = None
        if Tarjeta_Credito.validar_Tarjeta(num_tarjeta):
            tarjeta_credito = Tarjeta_Credito.obtener_tarjeta_Credito_numero(num_tarjeta, PagoTarjetaCreditoControlador.sesion)
            if tarjeta_credito is None:
                raise NumeroTarjetaIncorrecto("Número de tarjeta de crédito incorrecto")
        elif Tarjeta_Debito.validar_Tarjeta(num_tarjeta):
            tarjeta_debito = Tarjeta_Debito.obtener_tarjeta_Debito_numero(num_tarjeta, PagoTarjetaCreditoControlador.sesion)
            if tarjeta_debito is None:
                raise NumeroTarjetaIncorrecto("Número de tarjeta de débito incorrecto")
            tarjeta_credito = tarjeta_debito.obtener_tarjeta_credito_asociada(PagoTarjetaCreditoControlador.sesion)
            if tarjeta_credito is None:
                raise NumeroTarjetaIncorrecto("No se encontró una tarjeta de crédito asociada a la tarjeta de débito proporcionada")

        if tarjeta_credito:
            # Realizar el depósito
            tarjeta_credito.Saldo = float(tarjeta_credito.Saldo) + monto

            # Crear el movimiento de depósito
            tipo_deposito = PagoTarjetaCreditoControlador.sesion.query(Tipo_Movimiento).filter_by(Tipo='Depósito de efectivo').first()
            movimiento = Movimiento(
                Fecha=datetime.now(),
                Monto=monto,
                ID_Tipo_Movimiento=tipo_deposito.ID_Tipo_Movimiento
            )
            PagoTarjetaCreditoControlador.sesion.add(movimiento)

            # Relacionar el movimiento con la cuenta
            cuenta_movimiento = Cuenta_Movimiento(
                Num_Cuenta=tarjeta_credito.Num_Cuenta,
                Movimiento=movimiento
            )
            PagoTarjetaCreditoControlador.sesion.add(cuenta_movimiento)

            PagoTarjetaCreditoControlador.sesion.commit()
            return True

        else:
            raise NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")

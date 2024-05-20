from modelos.Tarjeta import Tarjeta_Credito, Tarjeta_Debito
from excepciones import excepciones_tarjeta
from excepciones import excepciones_billete
from modelos.Billete import Billete
from bd.db_controlador import sesion
from modelos.Movimiento import Movimiento
from datetime import datetime
from modelos.CuentaMovimiento import Cuenta_Movimiento
from modelos.Movimiento import MovimientoPagoServicio

class PagoServicioControlador(): 
    """
    Controlador para la gestión de pagos de servicios.

    Attributes:
        None
    """

    @staticmethod
    def pagar_servicio_con_tarjeta(num_tarjeta, monto, nip, num_convenio, referencia):
        """
        Realiza un pago de servicio con tarjeta.

        Args:
            num_tarjeta (str): Número de tarjeta.
            monto (float): Monto del pago.
            nip (str): NIP de la tarjeta.
            num_convenio (str): Número de convenio del servicio.
            referencia (str): Referencia del pago.

        Raises:
            excepciones_tarjeta.NumeroTarjetaIncorrecto: Si el número de tarjeta es incorrecto.
            excepciones_tarjeta.NipIncorrecto: Si el NIP es incorrecto.
            excepciones_tarjeta.SaldoInsuficiente: Si el saldo de la tarjeta es insuficiente para el pago.

        Returns:
            MovimientoPagoServicio: Objeto del movimiento de pago de servicio.
        """
        # Verificar si es una tarjeta de crédito válida
        if Tarjeta_Credito.validar_Tarjeta(num_tarjeta):
            tarjeta_credito = Tarjeta_Credito.obtener_tarjeta_Credito_numero(num_tarjeta, sesion)
            if tarjeta_credito is None:
                raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de crédito incorrecto")
            if not tarjeta_credito.check_nip(nip):
                raise excepciones_tarjeta.NipIncorrecto("NIP incorrecto")
            if (float(tarjeta_credito.Saldo) + monto) > float(tarjeta_credito.LimiteCredito):
                raise excepciones_tarjeta.SaldoInsuficiente("Saldo insuficiente para realizar el pago")

            tarjeta_credito.Saldo = float(tarjeta_credito.Saldo) + monto

            # Obtener la cuenta asociada a la tarjeta
            cuenta = tarjeta_credito.Cuenta

        # Verificar si es una tarjeta de débito válida
        elif Tarjeta_Debito.validar_Tarjeta(num_tarjeta):
            tarjeta_debito = Tarjeta_Debito.obtener_tarjeta_Debito_numero(num_tarjeta, sesion)
            if tarjeta_debito is None:
                raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de débito incorrecto")
            if not tarjeta_debito.check_nip(nip):
                raise excepciones_tarjeta.NipIncorrecto("NIP incorrecto")
            if float(tarjeta_debito.Saldo) < monto:  # Verificar saldo
                raise excepciones_tarjeta.SaldoInsuficiente("Saldo insuficiente para realizar el pago")

            tarjeta_debito.Saldo = float(tarjeta_debito.Saldo) - monto

            # Obtener la cuenta asociada a la tarjeta
            cuenta = tarjeta_debito.Cuenta

        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")

        # Registro del movimiento de pago de servicio
        movimiento = Movimiento(Fecha=datetime.now(), Monto=monto, ID_Tipo_Movimiento=4)  # 4 corresponde al pago de servicio
        sesion.add(movimiento)
        sesion.commit()

        # Asociar el movimiento con la cuenta
        cuenta_movimiento = Cuenta_Movimiento(Num_Cuenta=cuenta.Num_Cuenta, ID_Movimiento=movimiento.ID_Movimiento)
        sesion.add(cuenta_movimiento)
        sesion.commit()

        # Registro del pago de servicio
        movimiento_pago_servicio = MovimientoPagoServicio(
            ID_Movimiento=movimiento.ID_Movimiento,
            Num_Convenio=num_convenio,
            Referencia=referencia
        )
        sesion.add(movimiento_pago_servicio)
        sesion.commit()

        return movimiento_pago_servicio

    @staticmethod
    def pagar_servicio_sin_tarjeta(monto, num_convenio, referencia):
        """
        Realiza un pago de servicio sin tarjeta.

        Args:
            monto (float): Monto del pago.
            num_convenio (str): Número de convenio del servicio.
            referencia (str): Referencia del pago.

        Raises:
            excepciones_billete.DenominacionNoExistente: Si la denominación del billete no existe.

        Returns:
            MovimientoPagoServicio: Objeto del movimiento de pago de servicio.
        """
        # Lista de denominaciones en orden descendente
        denominaciones = [1000, 500, 200, 100, 50, 20]

        for denominacion in denominaciones:
            if monto >= denominacion:
                cantidad_a_depositar = monto // denominacion
                try:
                    Billete.agregar_billete(denominacion, cantidad_a_depositar, sesion)
                    monto -= cantidad_a_depositar * denominacion
                except excepciones_billete.DenominacionNoExistente:
                    continue

        # Registro del movimiento de pago de servicio
        movimiento = Movimiento(Fecha=datetime.now(), Monto=monto, ID_Tipo_Movimiento=4)  # 4 corresponde al pago de servicio
        sesion.add(movimiento)
        sesion.commit()

        # Registro del pago de servicio
        movimiento_pago_servicio = MovimientoPagoServicio(
            ID_Movimiento=movimiento.ID_Movimiento,
            Num_Convenio=num_convenio,
            Referencia=referencia
        )
        sesion.add(movimiento_pago_servicio)
        sesion.commit()

        return movimiento_pago_servicio

from modelos.Tarjeta import Tarjeta_Credito, Tarjeta_Debito
from excepciones import excepciones_tarjeta
from excepciones import excepciones_billete
from modelos.Billete import Billete
from bd.db_controlador import sesion
from modelos.Movimiento import Movimiento
from datetime import datetime
from modelos.CuentaMovimiento import Cuenta_Movimiento

class RetiroControlador(): 
    """
    Controlador para la gestión de retiros de efectivo.

    Attributes:
        None
    """

    @staticmethod
    def retirar(num_tarjeta, monto, nip):
        """
        Realiza un retiro de efectivo.

        Args:
            num_tarjeta (str): Número de tarjeta.
            monto (float): Monto del retiro.
            nip (str): NIP de la tarjeta.

        Raises:
            excepciones_tarjeta.NumeroTarjetaIncorrecto: Si el número de tarjeta es incorrecto.
            excepciones_tarjeta.NipIncorrecto: Si el NIP es incorrecto.
            excepciones_tarjeta.SaldoInsuficiente: Si el saldo de la tarjeta es insuficiente para el retiro.
            excepciones_billete.NoSePuedeDarMontoException: Si no es posible entregar el monto solicitado con los billetes disponibles.

        Returns:
            list: Lista de billetes entregados en el retiro.
        """
        # Verificar si es una tarjeta de crédito válida
        if Tarjeta_Credito.validar_Tarjeta(num_tarjeta):
            tarjeta_credito = Tarjeta_Credito.obtener_tarjeta_Credito_numero(num_tarjeta, sesion)
            if tarjeta_credito is None:
                raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de crédito incorrecto")
            if not tarjeta_credito.check_nip(nip):
                raise excepciones_tarjeta.NipIncorrecto("NIP incorrecto")
            if (float(tarjeta_credito.Saldo) + monto) > float(tarjeta_credito.LimiteCredito):
                raise excepciones_tarjeta.SaldoInsuficiente("Saldo insuficiente para realizar el retiro")
            if not Billete.puede_dar_monto(session= sesion, monto= monto):
                raise excepciones_billete.NoSePuedeDarMontoException

            # Realizar el retiro y obtener los billetes entregados
            billetes = Billete.dar_monto_mas_eficiente(sesion, monto)
            tarjeta_credito.Saldo += monto

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
                raise excepciones_tarjeta.SaldoInsuficiente("Saldo insuficiente para realizar el retiro")
            if not Billete.puede_dar_monto(session= sesion, monto= monto):
                raise excepciones_billete.NoSePuedeDarMontoException

            # Realizar el retiro y obtener los billetes entregados
            billetes = Billete.dar_monto_mas_eficiente(sesion, monto)
            tarjeta_debito.Saldo -= monto

            # Obtener la cuenta asociada a la tarjeta
            cuenta = tarjeta_debito.Cuenta

        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")

        # Registro del movimiento de retiro
        movimiento = Movimiento(Fecha=datetime.now(), Monto=monto, ID_Tipo_Movimiento=1)  # 1 corresponde al retiro de efectivo
        sesion.add(movimiento)
        sesion.commit()

        # Asociar el movimiento con la cuenta
        cuenta_movimiento = Cuenta_Movimiento(Num_Cuenta=cuenta.Num_Cuenta, ID_Movimiento=movimiento.ID_Movimiento)
        sesion.add(cuenta_movimiento)
        sesion.commit()

        return billetes



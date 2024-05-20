from modelos.Tarjeta import Tarjeta_Credito, Tarjeta_Debito
from sqlalchemy.orm import sessionmaker
from excepciones import excepciones_tarjeta
from excepciones import excepciones_billete
from modelos.Billete import Billete
from bd.db_controlador import sesion
from decimal import Decimal

class RetiroControlador(): 

    @staticmethod
    def retirar(num_tarjeta, monto, nip):
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

            billetes = Billete.dar_monto_mas_eficiente(sesion, monto)
            tarjeta_credito.Saldo += monto
            sesion.commit()
            return billetes
        
        # Verificar si es una tarjeta de débito válida
        elif Tarjeta_Debito.validar_Tarjeta(num_tarjeta):
            tarjeta_debito = Tarjeta_Debito.obtener_tarjeta_Debito_numero(num_tarjeta, sesion)
            if tarjeta_debito is None:
                raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de débito incorrecto")
            if not tarjeta_debito.check_nip(nip):
                raise excepciones_tarjeta.NipIncorrecto("NIP incorrecto")
            if float(tarjeta_debito.Saldo) < monto:  # Verificar saldo
                raise excepciones_tarjeta.SaldoInsuficiente("Saldo insuficiente para realizar el retiro")
            if not Billete.puede_dar_monto(self= None,session = sesion, monto = monto):
                raise excepciones_billete.NoSePuedeDarMontoException

            billetes = Billete.dar_monto_mas_eficiente(sesion, monto)
            tarjeta_debito.Saldo -= monto
            sesion.commit()
            return billetes
        
        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")

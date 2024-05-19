from modelos.Tarjeta import Tarjeta_Credito, Tarjeta_Debito
from sqlalchemy.orm import sessionmaker
from main import engine
from excepciones import excepciones_tarjeta
from excepciones import excepciones_billete
from modelos.Billete import Billete

class RetiroControlador(): 
    
    Session = sessionmaker(bind=engine)
    sesion = Session()

    @staticmethod
    def retirar(num_tarjeta, monto, nip):
        # Verificar si es una tarjeta de crédito válida
        if Tarjeta_Credito.validar_Tarjeta(num_tarjeta):
            tarjeta_credito = Tarjeta_Credito.obtener_tarjeta_Credito_numero(num_tarjeta, RetiroControlador.sesion)
            if tarjeta_credito is None:
                raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de crédito incorrecto")
            if not tarjeta_credito.check_nip(nip):
                raise excepciones_tarjeta.NipIncorrecto("NIP incorrecto")
            if (tarjeta_credito.Saldo + monto) > tarjeta_credito.LimiteCredito:
                raise excepciones_tarjeta.SaldoInsuficiente("Saldo insuficiente para realizar el retiro")
            if not Billete.puede_dar_monto(session= RetiroControlador.sesion, monto= monto):
                raise excepciones_billete.NoSePuedeDarMontoException

            billetes = Billete.dar_monto_mas_eficiente(RetiroControlador.sesion, monto)
            tarjeta_credito.Saldo += monto
            RetiroControlador.sesion.commit()
            return billetes
        
        # Verificar si es una tarjeta de débito válida
        elif Tarjeta_Debito.validar_Tarjeta(num_tarjeta):
            tarjeta_debito = Tarjeta_Debito.obtener_tarjeta_Debito_numero(num_tarjeta, RetiroControlador.sesion)
            if tarjeta_debito is None:
                raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de débito incorrecto")
            if not tarjeta_debito.check_nip(nip):
                raise excepciones_tarjeta.NipIncorrecto("NIP incorrecto")
            if tarjeta_debito.Saldo < monto:
                raise excepciones_tarjeta.SaldoInsuficiente("Saldo insuficiente para realizar el retiro")
            if not Billete.puede_dar_monto(session= RetiroControlador.sesion, monto= monto):
                raise excepciones_billete.NoSePuedeDarMontoException

            billetes = Billete.dar_monto_mas_eficiente(RetiroControlador.sesion, monto)
            tarjeta_debito.Saldo -= monto
            RetiroControlador.sesion.commit()
            return billetes
        
        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")

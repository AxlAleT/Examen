from modelos.Tarjeta import Tarjeta_Credito, Tarjeta_Debito
from excepciones import excepciones_tarjeta
from bd.db_controlador import sesion

class TarjetaControlador:

    @staticmethod
    def determinar_tipo_tarjeta(num_tarjeta):
        if Tarjeta_Debito.validar_Tarjeta(num_tarjeta):
            return 'debito'
        elif Tarjeta_Credito.validar_Tarjeta(num_tarjeta):
            return 'credito'
        else:
            return None

    @staticmethod
    def validar_numero_tarjeta(num_tarjeta): 
        return Tarjeta_Debito.validar_Tarjeta(num_tarjeta) or Tarjeta_Credito.validar_Tarjeta(num_tarjeta)

    @staticmethod
    def obtener_tarjeta(num_tarjeta):
        tipo_tarjeta = TarjetaControlador.determinar_tipo_tarjeta(num_tarjeta)
        if tipo_tarjeta == 'debito':
            return Tarjeta_Debito.obtener_tarjeta_Debito_numero(num_tarjeta, sesion)
        elif tipo_tarjeta == 'credito':
            return Tarjeta_Credito.obtener_tarjeta_Credito_numero(num_tarjeta, sesion)
        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")

    @staticmethod
    def validar_nip(num_tarjeta, nip):
        tarjeta = TarjetaControlador.obtener_tarjeta(num_tarjeta)
        if not tarjeta.check_nip(nip):
            raise excepciones_tarjeta.NipIncorrecto("NIP incorrecto")
        return True

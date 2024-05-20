from modelos.Tarjeta import Tarjeta_Credito, Tarjeta_Debito
from excepciones import excepciones_tarjeta
from bd.db_controlador import sesion

class TarjetaControlador:
    """
    Controlador para operaciones relacionadas con tarjetas.

    Attributes:
        None
    """
    @staticmethod
    def determinar_tipo_tarjeta(num_tarjeta):
        """
        Determina el tipo de tarjeta basado en su número.

        Args:
            num_tarjeta (str): Número de tarjeta.

        Returns:
            str: 'debito' si es una tarjeta de débito, 'credito' si es una tarjeta de crédito, o None si no es válida.
        """
        if Tarjeta_Debito.validar_Tarjeta(num_tarjeta):
            return 'debito'
        elif Tarjeta_Credito.validar_Tarjeta(num_tarjeta):
            return 'credito'
        else:
            return None

    @staticmethod
    def validar_numero_tarjeta(num_tarjeta): 
        """
        Valida si un número de tarjeta es válido.

        Args:
            num_tarjeta (str): Número de tarjeta.

        Returns:
            bool: True si el número de tarjeta es válido, False en caso contrario.
        """
        return Tarjeta_Debito.validar_Tarjeta(num_tarjeta) or Tarjeta_Credito.validar_Tarjeta(num_tarjeta)

    @staticmethod
    def obtener_tarjeta(num_tarjeta):
        """
        Obtiene la tarjeta correspondiente al número dado.

        Args:
            num_tarjeta (str): Número de tarjeta.

        Returns:
            Tarjeta: Objeto de tarjeta (Tarjeta_Credito o Tarjeta_Debito) correspondiente al número dado.

        Raises:
            excepciones_tarjeta.NumeroTarjetaIncorrecto: Si el número de tarjeta es incorrecto o no existe.
        """
        tipo_tarjeta = TarjetaControlador.determinar_tipo_tarjeta(num_tarjeta)
        if tipo_tarjeta == 'debito':
            return Tarjeta_Debito.obtener_tarjeta_Debito_numero(num_tarjeta, sesion)
        elif tipo_tarjeta == 'credito':
            return Tarjeta_Credito.obtener_tarjeta_Credito_numero(num_tarjeta, sesion)
        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")

    @staticmethod
    def validar_nip(num_tarjeta, nip):
        """
        Valida el NIP de una tarjeta.

        Args:
            num_tarjeta (str): Número de tarjeta.
            nip (str): NIP a validar.

        Returns:
            bool: True si el NIP es correcto, False si es incorrecto.

        Raises:
            excepciones_tarjeta.NipIncorrecto: Si el NIP es incorrecto.
        """
        tarjeta = TarjetaControlador.obtener_tarjeta(num_tarjeta)
        if not tarjeta.check_nip(nip):
            raise excepciones_tarjeta.NipIncorrecto("NIP incorrecto")
        return True

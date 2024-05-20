from modelos.Tarjeta import Tarjeta_Credito, Tarjeta_Debito
from excepciones import excepciones_tarjeta
from bd.db_controlador import sesion

class CambioNIPControlador:
    """
    Controlador para la gestión de cambios de NIP.

    Attributes:
        None
    """

    @staticmethod
    def cambiar_nip(num_tarjeta, nip_actual, nuevo_nip):
        """
        Cambia el NIP de una tarjeta.

        Args:
            num_tarjeta (str): Número de tarjeta.
            nip_actual (str): NIP actual de la tarjeta.
            nuevo_nip (str): Nuevo NIP de la tarjeta.

        Raises:
            excepciones_tarjeta.NumeroTarjetaIncorrecto: Si el número de tarjeta es incorrecto.
            excepciones_tarjeta.NipIncorrecto: Si el NIP actual es incorrecto.
            excepciones_tarjeta.NipInvalido: Si el nuevo NIP no cumple con los requisitos.

        Returns:
            bool: True si el cambio de NIP se realizó con éxito, False en caso contrario.
        """
        # Verificar si es una tarjeta de crédito válida
        if Tarjeta_Credito.validar_Tarjeta(num_tarjeta):
            tarjeta = Tarjeta_Credito.obtener_tarjeta_Credito_numero(num_tarjeta, sesion)
            if tarjeta is None:
                raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de crédito incorrecto")
        # Verificar si es una tarjeta de débito válida
        elif Tarjeta_Debito.validar_Tarjeta(num_tarjeta):
            tarjeta = Tarjeta_Debito.obtener_tarjeta_Debito_numero(num_tarjeta, sesion)
            if tarjeta is None:
                raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta de débito incorrecto")
        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")

        # Verificar el NIP actual
        if not tarjeta.check_nip(nip_actual):
            raise excepciones_tarjeta.NipIncorrecto("NIP actual incorrecto")

        # Verificar que el nuevo NIP sea válido (aquí se puede agregar cualquier lógica adicional para validar el nuevo NIP)
        if not nuevo_nip or len(nuevo_nip) < 4:
            raise excepciones_tarjeta.NipInvalido("El nuevo NIP no cumple con los requisitos")

        # Establecer el nuevo NIP
        tarjeta.set_nip(nuevo_nip)
        sesion.commit()

        return True

class NoSePuedeDarMontoException(Exception):
    pass
    """
    Excepción lanzada cuando no es posible entregar un monto solicitado con los billetes disponibles.
    """
class NoHaySolucionEficienteException(Exception):
    pass
    """
    Excepción lanzada cuando no hay una solución eficiente para entregar el monto solicitado con los billetes disponibles.
    """
class DenominacionNoExistente(Exception):
    pass
    """
    Excepción lanzada cuando se intenta agregar un billete de una denominación que no existe en el sistema.
    """

class NumeroTarjetaIncorrecto(Exception):
    """
    Excepción lanzada cuando se proporciona un número de tarjeta incorrecto o inválido.
    """
    pass

class NipIncorrecto(Exception):
    """
    Excepción lanzada cuando se proporciona un NIP incorrecto para una tarjeta.
    """
    pass

class SaldoInsuficiente(Exception):
    """
    Excepción lanzada cuando el saldo de una tarjeta no es suficiente para realizar una operación.
    """
    pass

from sqlalchemy import Column, Integer, CheckConstraint
from bd.base import Base
from excepciones.excepciones_billete import DenominacionNoExistente

class Billete(Base):
    """
    Clase que representa un billete en la base de datos.

    Attributes:
        ID_Billete (int): Identificador único del billete.
        Denominacion (int): Valor nominal del billete.
        Cantidad (int): Cantidad de billetes disponibles.
    """
    __tablename__ = "Billete"

    ID_Billete = Column(Integer, primary_key=True, nullable=False, unique=True)
    Denominacion = Column(Integer, CheckConstraint('Denominacion >= 20 AND Denominacion <= 1000'), nullable=False)
    Cantidad = Column(Integer)

    @staticmethod
    def agregar_billete(denominacion, cantidad, sesion):
        """
        Agrega billetes a la base de datos.

        Args:
            denominacion (int): Valor nominal del billete a agregar.
            cantidad (int): Cantidad de billetes a agregar.
            sesion (Session): Sesión de base de datos para realizar la transacción.

        Returns:
            Billete: El objeto de billete creado o actualizado.

        Raises:
            DenominacionNoExistente: Si la denominación del billete no existe en los registros.
        """
        billete = sesion.query(Billete).filter_by(Denominacion=denominacion).first()
        if billete:
            billete.Cantidad += cantidad
            sesion.commit()
            return billete
        else:
            raise DenominacionNoExistente(f"No se puede introducir billete de {denominacion} porque no existe en los registros.")

    def puede_dar_monto(self, session, monto):
        """
        Verifica si es posible entregar un monto específico utilizando los billetes disponibles.

        Args:
            session (Session): Sesión de base de datos para realizar la consulta.
            monto (int): Monto que se desea verificar.

        Returns:
            bool: True si es posible entregar el monto, False si no es posible.
        """
        billetes = session.query(Billete).all()
        return Billete._puede_dar_monto_con_billetes(billetes=billetes, monto=monto)

    def _puede_dar_monto_con_billetes(billetes, monto):
        """
        Función interna para verificar si es posible entregar un monto específico utilizando los billetes disponibles.

        Args:
            billetes (list): Lista de objetos Billete disponibles.
            monto (int): Monto que se desea verificar.

        Returns:
            bool: True si es posible entregar el monto, False si no es posible.
        """
        if monto == 0:
            return True
        if monto < 0:
            return False

        for billete in billetes:
            if billete.Cantidad > 0 and monto >= billete.Denominacion:
                billete.Cantidad -= 1
                if Billete._puede_dar_monto_con_billetes(billetes, monto - billete.Denominacion):
                    return True
                billete.Cantidad += 1

        return False

    @staticmethod
    def dar_monto_mas_eficiente(session, monto):
        """
        Encuentra la combinación más eficiente de billetes para entregar un monto específico.

        Args:
            session (Session): Sesión de base de datos para realizar la consulta.
            monto (int): Monto que se desea entregar.

        Returns:
            list: Lista de tuplas que contienen el valor nominal del billete y la cantidad necesaria para entregar el monto.

        Notes:
            Si no es posible entregar el monto con los billetes disponibles, devuelve None.
        """
        billetes = session.query(Billete).all()
        resultado = Billete._dar_monto_programacion_dinamica_con_billetes(billetes, monto)
        if resultado is None:
            return None
        else:
            return [(billete.Denominacion, cantidad) for billete, cantidad in resultado]

    @staticmethod
    def _dar_monto_programacion_dinamica_con_billetes(billetes, monto):
        """
        Utiliza programación dinámica para encontrar la combinación más eficiente de billetes para entregar un monto específico.

        Args:
            billetes (list): Lista de objetos Billete disponibles.
            monto (int): Monto que se desea entregar.

        Returns:
            list: Lista de tuplas que contienen el billete y la cantidad necesaria para entregar el monto.

        Notes:
            Si no es posible entregar el monto con los billetes disponibles, devuelve None.
        """
        dp = [None] * (monto + 1)
        dp[0] = []

        for current_monto in range(1, monto + 1):
            for billete in billetes:
                if billete.Cantidad > 0 and current_monto >= billete.Denominacion:
                    previous_monto = current_monto - billete.Denominacion
                    if dp[previous_monto] is not None:
                        nueva_cantidad = min(billete.Cantidad, monto // billete.Denominacion)
                        if dp[current_monto] is None or len(dp[previous_monto]) + 1 < len(dp[current_monto]):
                            dp[current_monto] = dp[previous_monto] + [(billete, nueva_cantidad)]

        return dp[monto]

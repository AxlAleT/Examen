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
    Denominacion = Column(Integer, CheckConstraint('Denominacion IN (20, 50, 100, 200, 500, 1000)'), nullable=False)
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

    @staticmethod
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
        denominaciones = [(billete.Denominacion, billete.Cantidad) for billete in billetes]
        resultado = Billete.calcular_cambio(denominaciones, monto)
        if not resultado:
            return None
        return resultado

    @staticmethod
    def calcular_cambio(denominaciones, monto):
        """
        Calcula el cambio necesario para un monto específico utilizando las denominaciones disponibles.

        Args:
            denominaciones (list): Lista de tuplas que contienen las denominaciones y la cantidad disponible de cada una.
            monto (int): Monto que se desea entregar.

        Returns:
            list: Lista de tuplas que contienen la denominación y la cantidad necesaria para entregar el monto.

        Notes:
            Si no es posible entregar el monto con las denominaciones disponibles, devuelve una lista vacía.
        """
        denominaciones.sort(reverse=True, key=lambda x: x[0])  # Ordenamos las denominaciones de mayor a menor
        cambio = []
        for denom, cant in denominaciones:
            if monto <= 0:
                break
            if cant > 0 and denom <= monto:
                cant_billetes = min(monto // denom, cant)  # Calculamos la cantidad de billetes de esta denominación que podemos usar
                monto -= cant_billetes * denom  # Restamos el valor de los billetes usados del monto total
                if cant_billetes > 0:
                    cambio.append((denom, cant_billetes))  # Añadimos los billetes utilizados al cambio
        if monto > 0:
            print("No se puede dar cambio completo.")
            return []
        return cambio



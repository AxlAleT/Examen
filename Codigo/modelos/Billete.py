from sqlalchemy import Column, Integer, CheckConstraint
from bd.base import Base
from sqlalchemy import desc
from excepciones.excepciones_billete import DenominacionNoExistente

class Billete(Base):
    __tablename__ = "Billete"

    ID_Billete = Column(Integer, primary_key=True, nullable=False, unique=True)
    Denominacion = Column(Integer, CheckConstraint('Denominacion >= 20 AND Denominacion <= 1000'), nullable=False)
    Cantidad = Column(Integer)

    @staticmethod
    def agregar_billete(denominacion, cantidad, sesion):
        billete = sesion.query(Billete).filter_by(Denominacion=denominacion).first()
        if billete:
            billete.Cantidad += cantidad
            sesion.commit()
            return billete
        else:
            raise DenominacionNoExistente(f"No se puede introducir billete de {denominacion} porque no existe en los registros.")

    def puede_dar_monto(self, session, monto):
        billetes = session.query(Billete).all()
        return Billete._puede_dar_monto_con_billetes(billetes= billetes,monto= monto)
    

    def _puede_dar_monto_con_billetes(billetes, monto):
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
        billetes = session.query(Billete).all()
        resultado = Billete._dar_monto_programacion_dinamica_con_billetes(billetes, monto)
        if resultado is None:
            return None
        else:
            return [(billete.Denominacion, cantidad) for billete, cantidad in resultado]

    @staticmethod
    def _dar_monto_programacion_dinamica_con_billetes(billetes, monto):
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
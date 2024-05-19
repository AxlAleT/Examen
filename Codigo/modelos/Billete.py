from sqlalchemy import Column, Integer, CheckConstraint
from bd.base import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class Billete(Base):
    __tablename__ = "Billete"

    ID_Billete = Column(Integer, primary_key=True, nullable=False, unique=True)
    Denominacion = Column(Integer, CheckConstraint('Denominacion >= 20 AND Denominacion <= 1000'), nullable=False)
    Cantidad = Column(Integer)


    def puede_dar_monto(self, session, monto):
        billetes = session.query(Billete).all()
        return self._puede_dar_monto_con_billetes(billetes, monto)
    

    def _puede_dar_monto_con_billetes(self, billetes, monto):
        if monto == 0:
            return True
        if monto < 0:
            return False

        for billete in billetes:
            if billete.Cantidad > 0 and monto >= billete.Denominacion:
                billete.Cantidad -= 1
                if self._puede_dar_monto_con_billetes(billetes, monto - billete.Denominacion):
                    return True
                billete.Cantidad += 1

        return False
    

    def dar_monto_mas_eficiente(self, session, monto):
        billetes = session.query(Billete).all()
        resultado = self._dar_monto_mas_eficiente_con_billetes(billetes, monto)
        if resultado is None:
            return None
        else:
            return [(billete.Denominacion, billete.Cantidad - nueva_cantidad) for billete, nueva_cantidad in resultado]
        

    def _dar_monto_mas_eficiente_con_billetes(self, billetes, monto):
        dp = [None] * (monto + 1)
        dp[0] = []

        for current_monto in range(1, monto + 1):
            for billete in billetes:
                if billete.Cantidad > 0 and current_monto >= billete.Denominacion:
                    previous_monto = current_monto - billete.Denominacion
                    if dp[previous_monto] is not None:
                        nueva_cantidad = billete.Cantidad - 1
                        if nueva_cantidad >= 0:
                            nueva_solucion = dp[previous_monto] + [(billete, nueva_cantidad)]
                            if dp[current_monto] is None or len(nueva_solucion) < len(dp[current_monto]):
                                dp[current_monto] = nueva_solucion

        return dp[monto]
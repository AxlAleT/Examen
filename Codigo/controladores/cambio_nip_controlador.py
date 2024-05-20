from sqlalchemy.orm import sessionmaker
from datetime import datetime
from modelos.Cuenta import Cuenta
from modelos.Tarjeta import Tarjeta_Debito
from modelos.Movimiento import Movimiento
from modelos.CuentaMovimiento import Cuenta_Movimiento
from modelos.Movimiento import Tipo_Movimiento
from excepciones.excepciones_tarjeta import NipIncorrecto, NumeroTarjetaIncorrecto

class CambioNIPControlador:
    @staticmethod
    def cambiar_nip(engine, num_cuenta, nuevo_nip):
        Session = sessionmaker(bind=engine)
        session = Session()

        cuenta = session.query(Cuenta).filter_by(Num_Cuenta=num_cuenta).first()
        if not cuenta:
            raise NumeroTarjetaIncorrecto(f'Cuenta con número {num_cuenta} no encontrada.')

        tarjeta_debito = session.query(Tarjeta_Debito).filter_by(Num_Cuenta=num_cuenta).first()
        if tarjeta_debito:
            tarjeta_debito.set_nip(nuevo_nip)
            session.add(tarjeta_debito)

            movimiento_cambio_nip = Movimiento(
                Fecha=datetime.now(),
                Monto=0.0,  # No hay monto en cambio de NIP
                ID_Tipo_Movimiento=session.query(Tipo_Movimiento).filter_by(Tipo='Cambio de NIP').first().ID_Tipo_Movimiento
            )
            session.add(movimiento_cambio_nip)

            cuenta_movimiento_cambio_nip = Cuenta_Movimiento(Cuenta=cuenta, Movimiento=movimiento_cambio_nip)
            session.add(cuenta_movimiento_cambio_nip)

            session.commit()
            session.close()
            return True
        else:
            session.close()
            raise NumeroTarjetaIncorrecto(f'Tarjeta de débito para la cuenta {num_cuenta} no encontrada.')

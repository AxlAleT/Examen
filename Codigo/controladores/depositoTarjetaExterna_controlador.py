# archivo: transferencia_controlador.py
from modelos.Tarjeta import Tarjeta_Credito, Tarjeta_Debito
from modelos.Movimiento import Movimiento, Tipo_Movimiento
from modelos.CuentaMovimiento import Cuenta_Movimiento
from sqlalchemy.orm import sessionmaker
from main import engine
from excepciones import excepciones_tarjeta
from datetime import datetime

class TransferenciaControlador:
    
    Session = sessionmaker(bind=engine)
    sesion = Session()
    
    @staticmethod
    def transferir(num_tarjeta_origen, nip_origen, num_tarjeta_destino, monto):
        # Validar tarjeta de origen (puede ser de débito o crédito)
        tarjeta_origen = TransferenciaControlador.validar_tarjeta(num_tarjeta_origen, nip_origen, monto, es_origen=True)
        
        # Validar tarjeta de destino (solo puede ser de débito)
        tarjeta_destino = TransferenciaControlador.validar_tarjeta(num_tarjeta_destino, nip_origen, monto, es_origen=False)
        
        # Verificar saldo o límite de crédito en tarjeta de origen
        TransferenciaControlador.verificar_fondos(tarjeta_origen, monto)
        
        # Realizar la transferencia
        TransferenciaControlador.actualizar_saldos(tarjeta_origen, tarjeta_destino, monto)
        
        # Registrar los movimientos
        TransferenciaControlador.registrar_movimiento(tarjeta_origen, tarjeta_destino, monto)
        
        # Confirmar la transacción
        TransferenciaControlador.sesion.commit()
        return True

    @staticmethod
    def validar_tarjeta(num_tarjeta, nip, monto, es_origen):
        if Tarjeta_Debito.validar_Tarjeta(num_tarjeta):
            tarjeta = Tarjeta_Debito.obtener_tarjeta_Debito_numero(num_tarjeta, TransferenciaControlador.sesion)
        elif es_origen and Tarjeta_Credito.validar_Tarjeta(num_tarjeta):
            tarjeta = Tarjeta_Credito.obtener_tarjeta_Credito_numero(num_tarjeta, TransferenciaControlador.sesion)
        else:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")
        
        if tarjeta is None:
            raise excepciones_tarjeta.NumeroTarjetaIncorrecto("Número de tarjeta incorrecto")
        if es_origen and not tarjeta.check_nip(nip):
            raise excepciones_tarjeta.NipIncorrecto("NIP incorrecto")
        
        return tarjeta

    @staticmethod
    def verificar_fondos(tarjeta, monto):
        if isinstance(tarjeta, Tarjeta_Debito):
            if tarjeta.Saldo < monto:
                raise excepciones_tarjeta.SaldoInsuficiente("Saldo insuficiente en tarjeta de débito")
        elif isinstance(tarjeta, Tarjeta_Credito):
            if (tarjeta.Saldo + monto) > tarjeta.LimiteCredito:
                raise excepciones_tarjeta.SaldoInsuficiente("Saldo insuficiente en tarjeta de crédito")

    @staticmethod
    def actualizar_saldos(tarjeta_origen, tarjeta_destino, monto):
        if isinstance(tarjeta_origen, Tarjeta_Debito):
            tarjeta_origen.Saldo -= monto
        elif isinstance(tarjeta_origen, Tarjeta_Credito):
            tarjeta_origen.Saldo += monto

        tarjeta_destino.Saldo += monto
        TransferenciaControlador.sesion.add(tarjeta_origen)
        TransferenciaControlador.sesion.add(tarjeta_destino)

    @staticmethod
    def registrar_movimiento(tarjeta_origen, tarjeta_destino, monto):
        tipo_transferencia = TransferenciaControlador.sesion.query(Tipo_Movimiento).filter_by(Tipo='Transferencia').first()
        
        movimiento_origen = Movimiento(
            Fecha=datetime.now(),
            Monto=-monto,
            ID_Tipo_Movimiento=tipo_transferencia.ID_Tipo_Movimiento
        )
        TransferenciaControlador.sesion.add(movimiento_origen)
        
        movimiento_destino = Movimiento(
            Fecha=datetime.now(),
            Monto=monto,
            ID_Tipo_Movimiento=tipo_transferencia.ID_Tipo_Movimiento
        )
        TransferenciaControlador.sesion.add(movimiento_destino)
        
        cuenta_movimiento_origen = Cuenta_Movimiento(Cuenta=tarjeta_origen.Cuenta, Movimiento=movimiento_origen)
        cuenta_movimiento_destino = Cuenta_Movimiento(Cuenta=tarjeta_destino.Cuenta, Movimiento=movimiento_destino)
        
        TransferenciaControlador.sesion.add(cuenta_movimiento_origen)
        TransferenciaControlador.sesion.add(cuenta_movimiento_destino)

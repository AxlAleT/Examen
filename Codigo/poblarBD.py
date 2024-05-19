from sqlalchemy.orm import sessionmaker
from datetime import datetime
from modelos.Billete import Billete
from modelos.Cuenta import Cuenta
from modelos.Tarjeta import Tarjeta_Credito
from modelos.Tarjeta import Tarjeta_Debito
from modelos.Servicio import Servicio
from modelos.Movimiento import Tipo_Movimiento
from modelos.Movimiento import Movimiento
from modelos.CuentaMovimiento import Cuenta_Movimiento
from random import choice
from modelos.Movimiento import MovimientoPagoServicio

def poblar(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear y agregar 10 registros
    cuentas = [
        Cuenta(Num_Cuenta=1234567890, CuentaHabiente='Juan Perez', Direccion='1234 Elm Street'),
        Cuenta(Num_Cuenta=2345678901, CuentaHabiente='Maria Lopez', Direccion='5678 Oak Street'),
        Cuenta(Num_Cuenta=3456789012, CuentaHabiente='Carlos Gonzalez', Direccion='9101 Pine Street'),
        Cuenta(Num_Cuenta=4567890123, CuentaHabiente='Luisa Martinez', Direccion='1213 Maple Street'),
        Cuenta(Num_Cuenta=5678901234, CuentaHabiente='Ana Fernandez', Direccion='1415 Cedar Street'),
        Cuenta(Num_Cuenta=6789012345, CuentaHabiente='Jose Ramirez', Direccion='1617 Birch Street'),
        Cuenta(Num_Cuenta=7890123456, CuentaHabiente='Sofia Herrera', Direccion='1819 Walnut Street'),
        Cuenta(Num_Cuenta=8901234567, CuentaHabiente='Pedro Morales', Direccion='2021 Willow Street'),
        Cuenta(Num_Cuenta=9012345678, CuentaHabiente='Laura Gutierrez', Direccion='2223 Ash Street'),
        Cuenta(Num_Cuenta=1234509876, CuentaHabiente='Miguel Torres', Direccion='2425 Fir Street'),
    ]

    # Agregar las cuentas a la sesión
    session.add_all(cuentas)

    # Confirmar las transacciones
    session.commit()

    for cuenta in cuentas:
        tarjeta_debito = Tarjeta_Debito(
            NumeroTarjeta=int(f'400000{cuenta.Num_Cuenta}'),
            Saldo=0.0,
            Num_Cuenta=cuenta.Num_Cuenta
        )
        tarjeta_debito.set_nip('1234')  # Establecer un NIP de ejemplo
        session.add(tarjeta_debito)

    # Crear y agregar 5 tarjetas de crédito para 5 de las cuentas
    for i, cuenta in enumerate(cuentas[:5]):
        tarjeta_credito = Tarjeta_Credito(
            NumeroTarjeta=int(f'500000{cuenta.Num_Cuenta}'),
            Saldo=0.0,
            LimiteCredito=10000.0,  # Ejemplo de límite de crédito
            Num_Cuenta=cuenta.Num_Cuenta
        )
        tarjeta_credito.set_nip('1234')  # Establecer un NIP de ejemplo
        session.add(tarjeta_credito)

    session.commit()

    denominaciones = [20, 50, 100, 200, 500, 1000]

    # Agregar billetes a la tabla
    for denom in denominaciones:
        billete = Billete(Denominacion=denom, Cantidad=100)
        session.add(billete)

    session.commit()


    servicios = [
        {"Num_Convenio": 100001, "NombreServicio": "Luz", "Descripcion": "Servicio de electricidad"},
        {"Num_Convenio": 100002, "NombreServicio": "Agua", "Descripcion": "Servicio de suministro de agua potable"},
        {"Num_Convenio": 100003, "NombreServicio": "Gas", "Descripcion": "Servicio de suministro de gas"},
        {"Num_Convenio": 100004, "NombreServicio": "Internet", "Descripcion": "Servicio de conexión a Internet"},
        {"Num_Convenio": 100005, "NombreServicio": "Teléfono", "Descripcion": "Servicio de telefonía"},
        {"Num_Convenio": 100006, "NombreServicio": "Cable", "Descripcion": "Servicio de televisión por cable"},
        {"Num_Convenio": 100007, "NombreServicio": "Mantenimiento", "Descripcion": "Servicio de mantenimiento del hogar"},
        {"Num_Convenio": 100008, "NombreServicio": "Seguridad", "Descripcion": "Servicio de seguridad del hogar"},
        {"Num_Convenio": 100009, "NombreServicio": "Limpieza", "Descripcion": "Servicio de limpieza del hogar"},
        {"Num_Convenio": 100010, "NombreServicio": "Jardinería", "Descripcion": "Servicio de jardinería del hogar"}
    ]

    # Agregar servicios a la tabla
    for servicio in servicios:
        nuevo_servicio = Servicio(**servicio)
        session.add(nuevo_servicio)

    # Confirmar cambios
    session.commit()


    tipos_movimiento = [
        Tipo_Movimiento(Tipo='Retiro de efectivo', Descripcion='Retiro de efectivo en cajero automático'),
        Tipo_Movimiento(Tipo='Depósito de efectivo', Descripcion='Depósito de efectivo en cuenta'),
        Tipo_Movimiento(Tipo='Pago de tarjeta de crédito', Descripcion='Pago de la tarjeta de crédito asociada'),
        Tipo_Movimiento(Tipo='Pago de servicios', Descripcion='Pago de servicios como luz, agua, etc.'),
        Tipo_Movimiento(Tipo='Consulta de saldo', Descripcion='Consulta del saldo disponible en la cuenta')
    ]

    # Agregar tipos de movimiento a la sesión
    session.add_all(tipos_movimiento)
    session.commit()

    # Obtener los IDs de los tipos de movimiento
    tipo_retiro_efectivo = session.query(Tipo_Movimiento).filter_by(Tipo='Retiro de efectivo').first().ID_Tipo_Movimiento
    tipo_deposito_efectivo = session.query(Tipo_Movimiento).filter_by(Tipo='Depósito de efectivo').first().ID_Tipo_Movimiento
    tipo_pago_tarjeta_credito = session.query(Tipo_Movimiento).filter_by(Tipo='Pago de tarjeta de crédito').first().ID_Tipo_Movimiento
    tipo_consulta_saldo = session.query(Tipo_Movimiento).filter_by(Tipo='Consulta de saldo').first().ID_Tipo_Movimiento

    # Agregar movimientos a las cuentas y crear la relación con la tabla intermedia
    for cuenta in session.query(Cuenta).all():
        # Crear movimientos de ejemplo
        movimiento_retiro = Movimiento(
            Fecha=datetime.now(),
            Monto=50.0,  # Monto de ejemplo
            ID_Tipo_Movimiento=tipo_retiro_efectivo
        )
        session.add(movimiento_retiro)

        movimiento_deposito = Movimiento(
            Fecha=datetime.now(),
            Monto=100.0,  # Monto de ejemplo
            ID_Tipo_Movimiento=tipo_deposito_efectivo
        )
        session.add(movimiento_deposito)

        movimiento_pago_tarjeta = Movimiento(
            Fecha=datetime.now(),
            Monto=200.0,  # Monto de ejemplo
            ID_Tipo_Movimiento=tipo_pago_tarjeta_credito
        )
        session.add(movimiento_pago_tarjeta)

        movimiento_consulta_saldo = Movimiento(
            Fecha=datetime.now(),
            Monto=0.0,  # No hay monto en consulta de saldo
            ID_Tipo_Movimiento=tipo_consulta_saldo
        )
        session.add(movimiento_consulta_saldo)

        # Crear la relación con la tabla intermedia
        cuenta_movimiento_retiro = Cuenta_Movimiento(Cuenta=cuenta, Movimiento=movimiento_retiro)
        cuenta_movimiento_deposito = Cuenta_Movimiento(Cuenta=cuenta, Movimiento=movimiento_deposito)
        cuenta_movimiento_pago_tarjeta = Cuenta_Movimiento(Cuenta=cuenta, Movimiento=movimiento_pago_tarjeta)
        cuenta_movimiento_consulta_saldo = Cuenta_Movimiento(Cuenta=cuenta, Movimiento=movimiento_consulta_saldo)

        session.add_all([cuenta_movimiento_retiro, cuenta_movimiento_deposito, cuenta_movimiento_pago_tarjeta, cuenta_movimiento_consulta_saldo])

    session.commit()

    # Cerrar la sesión
    session.close()
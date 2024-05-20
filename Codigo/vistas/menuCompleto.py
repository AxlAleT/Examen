import wx
from sqlalchemy import create_engine
from vistas.retiro_vista import Retiro
from vistas.cambio_nip_gui import CambioNIP

class MenuCompleto(wx.Frame):
    """Clase para el menú completo de la aplicación.

    Esta clase representa la ventana principal del menú completo, donde el usuario puede
    seleccionar diversas operaciones, como retiro de efectivo, depósito de efectivo, pago
    de tarjeta de crédito, pago de servicios, consulta de saldo y movimientos, y salir.

    Args:
        parent (wx.Window): La ventana principal de la aplicación.
        numero_tarjeta (str): El número de tarjeta del usuario, opcional.

    """
    def __init__(self, parent, numero_tarjeta=None):
        """Inicializa la ventana del menú completo.

        Args:
            parent (wx.Window): La ventana principal de la aplicación.
            numero_tarjeta (str): El número de tarjeta del usuario, opcional.

        """
        super().__init__(parent, title='Menú Completo', size=(300, 400))
        self.numero_tarjeta = numero_tarjeta  # Almacenar el número de tarjeta recibido
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        buttons = [
            ("Retiro de Efectivo", self.retirar_efectivo),
            ("Depósito de Efectivo", self.depositar_efectivo),
            ("Pago de Tarjeta de Crédito", self.pagar_tarjeta_credito),
            ("Pago de Servicios", self.pagar_servicios),
            ("Consulta de Saldo/Movimientos", self.consultar_saldo_movimientos),
            ("Cambiar NIP", self.cambiar_nip),
            ("Salir", self.salir)  # Botón Salir
        ]

        for label, handler in buttons:
            button = wx.Button(panel, label=label)
            button.Bind(wx.EVT_BUTTON, handler)
            vbox.Add(button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(vbox)
        self.Show()

    def retirar_efectivo(self, event):
        """Método para manejar el evento de retiro de efectivo.

        Este método crea y muestra la ventana de retiro de efectivo.

        Args:
            event: El evento que desencadenó la llamada al método.

        """
        retiro_frame = Retiro(self, numero_tarjeta=self.numero_tarjeta)
        retiro_frame.Show()

    def depositar_efectivo(self, event):
        """Método para manejar el evento de depósito de efectivo.

        Este método crea y muestra la ventana de depósito de efectivo.

        Args:
            event: El evento que desencadenó la llamada al método.

        """
        from vistas.deposito_vista import Deposito
        deposito = Deposito(self, numero_tarjeta= self.numero_tarjeta)
        deposito.Show()


    def pagar_tarjeta_credito(self, event):
        """Método para manejar el evento de pago de tarjeta de crédito.

        Este método crea y muestra la ventana de pago de tarjeta de crédito.

        Args:
            event: El evento que desencadenó la llamada al método.

        """
        from vistas.pago_TarjetaCredito_vista import PagoTarjetaCredito
        pagoTarjetaCredito = PagoTarjetaCredito(self, self.numero_tarjeta)
        pagoTarjetaCredito.Show()

    def pagar_servicios(self, event):
        """Método para manejar el evento de pago de servicios.

        Este método crea y muestra la ventana de selección de servicio para el pago.

        Args:
            event: El evento que desencadenó la llamada al método.

        """
        from vistas.seleccionarServicio import SeleccionarServicioParaTarjeta
        seleccionarServicioParaTarjeta = SeleccionarServicioParaTarjeta(self, num_tarjeta=self.numero_tarjeta)
        seleccionarServicioParaTarjeta.Show()

    def consultar_saldo_movimientos(self, event):
        """Método para manejar el evento de consulta de saldo y movimientos.

        Este método realiza la operación de consulta de saldo y movimientos.

        Args:
            event: El evento que desencadenó la llamada al método.

        """
        from vistas.saldosmov_vistas import ConsultaSaldo
        consultaSaldo = ConsultaSaldo(parent=self, num_tarjeta=self.numero_tarjeta)
        consultaSaldo.Show()
    
    def cambiar_nip(self, event):
        engine = create_engine('sqlite:///Codigo/bd/base.db')
        nip_frame = CambioNIP(parent= self, numero_tarjeta=self.numero_tarjeta)
        nip_frame.Show()

    def salir(self, event):
        """Método para manejar el evento de salir.

        Este método cierra la ventana actual.

        Args:
            event: El evento que desencadenó la llamada al método.

        """
        self.Close()  # Cierra la ventana actual




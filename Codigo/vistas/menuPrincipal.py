import wx
from vistas.insertarTarjeta import InsertarTarjeta

class MenuPrincipal(wx.Frame):
    """
    Clase que representa la ventana del menú principal de un cajero automático.

    Attributes:
        parent (wx.Window): La ventana padre de esta ventana.
    
    Methods:
        __init__(parent=None): Inicializa la ventana del menú principal.
        depositar_efectivo(event): Abre la ventana para realizar un depósito de efectivo.
        pagar_servicios(event): Abre la ventana para realizar el pago de servicios.
        abrir_insertar_tarjeta(event): Abre la ventana para insertar una tarjeta en el cajero.
    """

    def __init__(self, parent=None):
        """
        Inicializa la ventana del menú principal.

        Args:
            parent (wx.Window): La ventana padre de esta ventana. Por defecto es None.
        """
        super().__init__(parent, title='Cajero Automático')
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        buttons = [
            ("Depósito de Efectivo", self.depositar_efectivo),
            ("Pago de Servicios", self.pagar_servicios),
            ("Insertar Tarjeta", self.abrir_insertar_tarjeta),
        ]

        for label, handler in buttons:
            button = wx.Button(panel, label=label)
            button.Bind(wx.EVT_BUTTON, handler)
            vbox.Add(button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(vbox)
        self.Show()

    def depositar_efectivo(self, event):
        """
        Abre la ventana para realizar un depósito de efectivo.
        
        Args:
            event: El evento que activa la función (en este caso, el clic en el botón).
        """
        from vistas.deposito_sinTarjeta_vista import DepositoSinTarjeta
        deposito = DepositoSinTarjeta(parent=self)
        deposito.Show()

    def pagar_servicios(self, event):
        """
        Abre la ventana para realizar el pago de servicios.
        
        Args:
            event: El evento que activa la función (en este caso, el clic en el botón).
        """
        from vistas.seleccionarServicio import SeleccionarServicio
        seleccionarServicio = SeleccionarServicio(self)
        seleccionarServicio.Show()

    def abrir_insertar_tarjeta(self, event):
        """
        Abre la ventana para insertar una tarjeta en el cajero.
        
        Args:
            event: El evento que activa la función (en este caso, el clic en el botón).
        """
        insertar_tarjeta_frame = InsertarTarjeta(self)
        insertar_tarjeta_frame.Show()


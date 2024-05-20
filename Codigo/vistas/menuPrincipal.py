import wx
from vistas.insertarTarjeta import InsertarTarjeta

class MenuPrincipal(wx.Frame):
    def __init__(self, parent=None):
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
        from vistas.deposito_vista import Deposito
        deposito = Deposito(parent=self)
        deposito.Show()

    def pagar_servicios(self, event):
        from vistas.seleccionarServicio import SeleccionarServicio
        seleccionarServicio = SeleccionarServicio(self)
        seleccionarServicio.Show()

    def abrir_insertar_tarjeta(self, event):
        insertar_tarjeta_frame = InsertarTarjeta(self)
        insertar_tarjeta_frame.Show()

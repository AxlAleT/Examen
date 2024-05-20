import wx
from vistas.retiro_vista import Retiro
from vistas.cambio_nip_gui import CambioNIP

class MenuCompleto(wx.Frame):
    def __init__(self, parent, numero_tarjeta=None):
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
        ]

        for label, handler in buttons:
            button = wx.Button(panel, label=label)
            button.Bind(wx.EVT_BUTTON, handler)
            vbox.Add(button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(vbox)
        self.Show()

    def retirar_efectivo(self, event):
        retiro_frame = Retiro(self, numero_tarjeta= self.numero_tarjeta)
        retiro_frame.Show()

    def depositar_efectivo(self, event):
        print("Depósito de efectivo")
        # Aquí puedes utilizar self.numero_tarjeta según sea necesario

    def pagar_tarjeta_credito(self, event):
        print("Pago de tarjeta de crédito")
        # Aquí puedes utilizar self.numero_tarjeta según sea necesario

    def pagar_servicios(self, event):
        print("Pago de servicios")
        # Aquí puedes utilizar self.numero_tarjeta según sea necesario

    def consultar_saldo_movimientos(self, event):
        print("Consulta de saldo/movimientos")
        # Aquí puedes utilizar self.numero_tarjeta según sea necesario
    
    def cambiar_nip(self, event):
        nip_frame = CambioNIP(self, numero_tarjeta = self.numero_tarjeta)

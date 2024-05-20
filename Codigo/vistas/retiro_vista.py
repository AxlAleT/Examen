import wx

class Retiro(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title='Retiro', size=(300, 400))
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
        print("Retiro de efectivo")

    def depositar_efectivo(self, event):
        print("Depósito de efectivo")

    def pagar_tarjeta_credito(self, event):
        print("Pago de tarjeta de crédito")

    def pagar_servicios(self, event):
        print("Pago de servicios")

    def consultar_saldo_movimientos(self, event):
        print("Consulta de saldo/movimientos")

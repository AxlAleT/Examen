import wx
from vistas.retiro_vista import Retiro

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
            ("Salir", self.salir)  # Botón Salir
        ]

        for label, handler in buttons:
            button = wx.Button(panel, label=label)
            button.Bind(wx.EVT_BUTTON, handler)
            vbox.Add(button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(vbox)
        self.Show()

    def retirar_efectivo(self, event):
        retiro_frame = Retiro(self, numero_tarjeta=self.numero_tarjeta)
        retiro_frame.Show()

    def depositar_efectivo(self, event):
        from vistas.deposito_vista import Deposito
        deposito = Deposito(self, numero_tarjeta= self.numero_tarjeta)
        deposito.Show()


    def pagar_tarjeta_credito(self, event):
        print("Pago de tarjeta de crédito")
        # Aquí puedes utilizar self.numero_tarjeta según sea necesario

    def pagar_servicios(self, event):
        from vistas.seleccionarServicio import SeleccionarServicioParaTarjeta
        seleccionarServicioParaTarjeta = SeleccionarServicioParaTarjeta(self, num_tarjeta=self.numero_tarjeta)
        seleccionarServicioParaTarjeta.Show()

    def consultar_saldo_movimientos(self, event):
        print("Consulta de saldo/movimientos")
        # Aquí puedes utilizar self.numero_tarjeta según sea necesario

    def salir(self, event):
        self.Close()  # Cierra la ventana actual


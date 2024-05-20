import wx
from controladores.deposito_controlador import DepositoControlador
from excepciones.excepciones_tarjeta import NumeroTarjetaIncorrecto, NipIncorrecto

class Deposito(wx.Frame):
    def __init__(self, parent, numero_tarjeta=None):
        super().__init__(parent, title='Depósito de Efectivo', size=(300, 200))
        self.numero_tarjeta = numero_tarjeta
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_monto = wx.StaticText(panel, label='Monto a depositar:')
        self.text_monto = wx.TextCtrl(panel)
        hbox1.Add(label_monto, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_monto, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label_nip = wx.StaticText(panel, label='NIP:')
        self.text_nip = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        hbox2.Add(label_nip, 0, wx.ALL | wx.CENTER, 5)
        hbox2.Add(self.text_nip, 1, wx.ALL | wx.EXPAND, 5)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        button_depositar = wx.Button(panel, label='Depositar')
        button_depositar.Bind(wx.EVT_BUTTON, self.depositar_efectivo)
        hbox3.Add(button_depositar, 0, wx.ALL | wx.CENTER, 5)
        button_volver = wx.Button(panel, label='Volver al Menú Principal')
        button_volver.Bind(wx.EVT_BUTTON, self.volver_menu_principal)
        hbox3.Add(button_volver, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox3, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)

    def depositar_efectivo(self, event):
        monto_string = self.text_monto.GetValue()
        nip = self.text_nip.GetValue()
        monto = int(monto_string)
        try:
            DepositoControlador.depositar(self.numero_tarjeta, monto, nip)
            wx.MessageBox('Depósito realizado con éxito', 'Información', wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except NumeroTarjetaIncorrecto:
            wx.MessageBox('Número de tarjeta incorrecto', 'Error', wx.OK | wx.ICON_ERROR)
        except NipIncorrecto:
            wx.MessageBox('NIP incorrecto', 'Error', wx.OK | wx.ICON_ERROR)

    def volver_menu_principal(self, event):
        self.Close()

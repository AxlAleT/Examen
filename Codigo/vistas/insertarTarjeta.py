import wx
from vistas.menuCompleto import MenuCompleto
from controladores.tarjeta_controlador import TarjetaControlador
from excepciones.excepciones_tarjeta import NipIncorrecto

class InsertarTarjeta(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title='Insertar Tarjeta', size=(300, 200))
        self.parent = parent
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_tarjeta = wx.StaticText(panel, label='Número de Tarjeta:')
        self.text_tarjeta = wx.TextCtrl(panel)
        hbox1.Add(label_tarjeta, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_tarjeta, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label_nip = wx.StaticText(panel, label='NIP:')
        self.text_nip = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        hbox2.Add(label_nip, 0, wx.ALL | wx.CENTER, 5)
        hbox2.Add(self.text_nip, 1, wx.ALL | wx.EXPAND, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)

        button_validar = wx.Button(panel, label='Validar')
        button_validar.Bind(wx.EVT_BUTTON, self.validar_nip)
        vbox.Add(button_validar, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(vbox)

    def validar_nip(self, event):
        numero_tarjeta = self.text_tarjeta.GetValue()
        nip = self.text_nip.GetValue()
        tarjetaControlador = TarjetaControlador()

        if not tarjetaControlador.validar_numero_tarjeta(numero_tarjeta):
            wx.MessageBox('Número de tarjeta incorrecto', 'Error', wx.OK | wx.ICON_ERROR)
            return

        try:
            tarjetaControlador.validar_nip(numero_tarjeta, nip)
            wx.MessageBox('NIP correcto', 'Éxito', wx.OK | wx.ICON_INFORMATION)
            self.Close()
            self.parent.Close()
            menu_completo_frame = MenuCompleto(None)
            menu_completo_frame.Show()
        except NipIncorrecto as e:
            wx.MessageBox('NIP incorrecto', 'Error', wx.OK | wx.ICON_ERROR)

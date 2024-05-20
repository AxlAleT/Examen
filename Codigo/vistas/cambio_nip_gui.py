import wx
from controladores.cambio_nip_controlador import CambioNIPControlador
from excepciones.excepciones_tarjeta import NipIncorrecto, NumeroTarjetaIncorrecto

class CambioNIP(wx.Frame):
    def __init__(self, parent, engine, numero_tarjeta=None):
        super().__init__(parent, title='Cambio de NIP', size=(300, 200))
        self.engine = engine
        self.numero_tarjeta = numero_tarjeta  # Almacenar el número de tarjeta recibido
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_num_cuenta = wx.StaticText(panel, label='Número de Cuenta:')
        self.text_num_cuenta = wx.TextCtrl(panel)
        hbox1.Add(label_num_cuenta, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_num_cuenta, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label_nuevo_nip = wx.StaticText(panel, label='Nuevo NIP:')
        self.text_nuevo_nip = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        hbox2.Add(label_nuevo_nip, 0, wx.ALL | wx.CENTER, 5)
        hbox2.Add(self.text_nuevo_nip, 1, wx.ALL | wx.EXPAND, 5)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        button_cambiar = wx.Button(panel, label='Cambiar NIP')
        button_cambiar.Bind(wx.EVT_BUTTON, self.cambiar_nip)
        hbox3.Add(button_cambiar, 0, wx.ALL | wx.CENTER, 5)
        button_volver = wx.Button(panel, label='Volver al Menú Principal')
        button_volver.Bind(wx.EVT_BUTTON, self.volver_menu_principal)
        hbox3.Add(button_volver, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox3, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)

    def cambiar_nip(self, event):
        num_cuenta = self.text_num_cuenta.GetValue()
        nuevo_nip = self.text_nuevo_nip.GetValue()
        try:
            CambioNIPControlador.cambiar_nip(self.engine, num_cuenta, nuevo_nip)
            wx.MessageBox(f'NIP cambiado exitosamente para la cuenta {num_cuenta}.', 'Éxito', wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except NipIncorrecto as e:
            wx.MessageBox('NIP incorrecto', 'Error', wx.OK | wx.ICON_ERROR)
        except NumeroTarjetaIncorrecto as e:
            wx.MessageBox('Número de tarjeta incorrecto', 'Error', wx.OK | wx.ICON_ERROR)

    def volver_menu_principal(self, event):
        self.Close()




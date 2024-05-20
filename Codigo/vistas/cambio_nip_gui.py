import wx
from controladores.cambio_nip_controlador import CambioNIPControlador
from excepciones.excepciones_tarjeta import NipIncorrecto, NumeroTarjetaIncorrecto

class CambioNIP(wx.Frame):
    def __init__(self, parent, numero_tarjeta=None):
        super().__init__(parent, title='Cambio de NIP', size=(300, 200))
        self.numero_tarjeta = numero_tarjeta  # Almacenar el número de tarjeta recibido
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_num_tarjeta = wx.StaticText(panel, label='Número de Tarjeta:')
        self.text_num_tarjeta = wx.TextCtrl(panel)
        hbox1.Add(label_num_tarjeta, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_num_tarjeta, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label_nip_actual = wx.StaticText(panel, label='NIP Actual:')
        self.text_nip_actual = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        hbox2.Add(label_nip_actual, 0, wx.ALL | wx.CENTER, 5)
        hbox2.Add(self.text_nip_actual, 1, wx.ALL | wx.EXPAND, 5)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        label_nuevo_nip = wx.StaticText(panel, label='Nuevo NIP:')
        self.text_nuevo_nip = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        hbox3.Add(label_nuevo_nip, 0, wx.ALL | wx.CENTER, 5)
        hbox3.Add(self.text_nuevo_nip, 1, wx.ALL | wx.EXPAND, 5)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        button_cambiar = wx.Button(panel, label='Cambiar NIP', size = (120, 30))
        button_cambiar.Bind(wx.EVT_BUTTON, self.cambiar_nip)
        hbox4.Add(button_cambiar, 0, wx.ALL | wx.CENTER, 5)
        button_volver = wx.Button(panel, label='Volver al Menú Principal', size = (120, 30))
        button_volver.Bind(wx.EVT_BUTTON, self.volver_menu_principal)
        hbox4.Add(button_volver, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox3, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox4, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)

    def cambiar_nip(self, event):
        num_tarjeta = self.text_num_tarjeta.GetValue()
        nip_actual = self.text_nip_actual.GetValue()
        nuevo_nip = self.text_nuevo_nip.GetValue()
        try:
            CambioNIPControlador.cambiar_nip(num_tarjeta, nip_actual, nuevo_nip)
            wx.MessageBox(f'NIP cambiado exitosamente para la tarjeta {num_tarjeta}.', 'Éxito', wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except NipIncorrecto:
            wx.MessageBox('NIP actual incorrecto', 'Error', wx.OK | wx.ICON_ERROR)
        except NumeroTarjetaIncorrecto:
            wx.MessageBox('Número de tarjeta incorrecto', 'Error', wx.OK | wx.ICON_ERROR)
        
    def volver_menu_principal(self, event):
        self.Close()

if __name__ == '__main__':
    app = wx.App(False)
    frame = CambioNIP(None)
    frame.Show()
    app.MainLoop()

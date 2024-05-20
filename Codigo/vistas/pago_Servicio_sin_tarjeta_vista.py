# pago_servicio_sin_tarjeta.py
import wx
from controladores.pago_servicio_controlador import PagoServicioControlador
from excepciones.excepciones_billete import DenominacionNoExistente

class PagoServicioSinTarjeta(wx.Frame):
    def __init__(self, parent, num_convenio):
        super().__init__(parent, title='Pago de Servicio sin Tarjeta', size=(400, 250))
        self.num_convenio = num_convenio
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_monto = wx.StaticText(panel, label='Monto:')
        self.text_monto = wx.TextCtrl(panel)
        hbox1.Add(label_monto, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_monto, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label_referencia = wx.StaticText(panel, label='Referencia:')
        self.text_referencia = wx.TextCtrl(panel)
        hbox2.Add(label_referencia, 0, wx.ALL | wx.CENTER, 5)
        hbox2.Add(self.text_referencia, 1, wx.ALL | wx.EXPAND, 5)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        button_aceptar = wx.Button(panel, label='Aceptar')
        button_aceptar.Bind(wx.EVT_BUTTON, self.pagar_servicio)
        hbox3.Add(button_aceptar, 0, wx.ALL | wx.CENTER, 5)

        button_volver = wx.Button(panel, label='Volver')
        button_volver.Bind(wx.EVT_BUTTON, self.volver_menu_principal)
        hbox3.Add(button_volver, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox3, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(vbox)

    def pagar_servicio(self, event):
        try:
            monto = float(self.text_monto.GetValue())
            referencia = self.text_referencia.GetValue()
            movimiento_pago = PagoServicioControlador.pagar_servicio_sin_tarjeta(monto, self.num_convenio, referencia)
            wx.MessageBox('Pago realizado con éxito', 'Información', wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except DenominacionNoExistente as e:
            wx.MessageBox(str(e), 'Error', wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox('Error inesperado: ' + str(e), 'Error', wx.OK | wx.ICON_ERROR)

    def volver_menu_principal(self, event):
        self.Close()

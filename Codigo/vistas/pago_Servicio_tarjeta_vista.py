# pago_servicio_con_tarjeta_vista.py
import wx
from controladores.pago_servicio_controlador import PagoServicioControlador
from excepciones.excepciones_tarjeta import NipIncorrecto, SaldoInsuficiente, NumeroTarjetaIncorrecto

class PagoServicioConTarjeta(wx.Frame):
    def __init__(self, parent, num_tarjeta, num_convenio):
        super().__init__(parent, title='Pago de Servicio con Tarjeta', size=(400, 300))
        self.num_tarjeta = num_tarjeta
        self.num_convenio = num_convenio
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_nip = wx.StaticText(panel, label='NIP:')
        self.text_nip = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        hbox1.Add(label_nip, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_nip, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label_monto = wx.StaticText(panel, label='Monto:')
        self.text_monto = wx.TextCtrl(panel)
        hbox2.Add(label_monto, 0, wx.ALL | wx.CENTER, 5)
        hbox2.Add(self.text_monto, 1, wx.ALL | wx.EXPAND, 5)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        label_referencia = wx.StaticText(panel, label='Referencia:')
        self.text_referencia = wx.TextCtrl(panel)
        hbox3.Add(label_referencia, 0, wx.ALL | wx.CENTER, 5)
        hbox3.Add(self.text_referencia, 1, wx.ALL | wx.EXPAND, 5)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        button_aceptar = wx.Button(panel, label='Aceptar')
        button_aceptar.Bind(wx.EVT_BUTTON, self.pagar_servicio)
        hbox4.Add(button_aceptar, 0, wx.ALL | wx.CENTER, 5)
        button_volver = wx.Button(panel, label='Volver')
        button_volver.Bind(wx.EVT_BUTTON, self.volver)
        hbox4.Add(button_volver, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox3, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox4, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(vbox)
        self.Show()

    def pagar_servicio(self, event):
        nip = self.text_nip.GetValue()
        monto = float(self.text_monto.GetValue())
        referencia = self.text_referencia.GetValue()
        try:
            PagoServicioControlador.pagar_servicio_con_tarjeta(self.num_tarjeta, monto, nip, self.num_convenio, referencia)
            wx.MessageBox('Pago realizado con éxito', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except NumeroTarjetaIncorrecto as e:
            wx.MessageBox(str(e), 'Error', wx.OK | wx.ICON_ERROR)
        except NipIncorrecto as e:
            wx.MessageBox(str(e), 'Error', wx.OK | wx.ICON_ERROR)
        except SaldoInsuficiente as e:
            wx.MessageBox(str(e), 'Error', wx.OK | wx.ICON_ERROR)

    def volver(self, event):
        self.Close()
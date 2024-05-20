import wx
from controladores.saldosmov_controlador import ConsultaControlador
from excepciones.excepciones_tarjeta import NumeroTarjetaIncorrecto

class ConsultaSaldo(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title='Consulta de Saldo', size=(300, 200))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_numero_cuenta = wx.StaticText(panel, label='Número de Cuenta:')
        self.text_numero_cuenta = wx.TextCtrl(panel)
        hbox1.Add(label_numero_cuenta, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_numero_cuenta, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        button_consultar = wx.Button(panel, label='Consultar Saldo')
        button_consultar.Bind(wx.EVT_BUTTON, self.consultar_saldo)
        hbox2.Add(button_consultar, 0, wx.ALL | wx.CENTER, 5)
        button_volver = wx.Button(panel, label='Volver al Menú Principal')
        button_volver.Bind(wx.EVT_BUTTON, self.volver_menu_principal)
        hbox2.Add(button_volver, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)

    def consultar_saldo(self, event):
        numero_cuenta = self.text_numero_cuenta.GetValue()
        try: 
            saldo = ConsultaControlador.consultar_saldo(numero_cuenta)
            wx.MessageBox(f'Saldo Actual: ${saldo:.2f}', 'Consulta Exitosa', wx.OK | wx.ICON_INFORMATION)
        except NumeroTarjetaIncorrecto as e: 
            wx.MessageBox('Número de cuenta incorrecto', 'Error', wx.OK | wx.ICON_ERROR)

    def volver_menu_principal(self, event):
        self.Close()

class ConsultaMovimientos(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title='Consulta de Movimientos', size=(400, 300))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_numero_cuenta = wx.StaticText(panel, label='Número de Cuenta:')
        self.text_numero_cuenta = wx.TextCtrl(panel)
        hbox1.Add(label_numero_cuenta, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_numero_cuenta, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        button_consultar = wx.Button(panel, label='Consultar Movimientos')
        button_consultar.Bind(wx.EVT_BUTTON, self.consultar_movimientos)
        hbox2.Add(button_consultar, 0, wx.ALL | wx.CENTER, 5)
        button_volver = wx.Button(panel, label='Volver al Menú Principal')
        button_volver.Bind(wx.EVT_BUTTON, self.volver_menu_principal)
        hbox2.Add(button_volver, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)

    def consultar_movimientos(self, event):
        numero_cuenta = self.text_numero_cuenta.GetValue()
        try: 
            movimientos = ConsultaControlador.consultar_movimientos(numero_cuenta)
            if not movimientos:
                wx.MessageBox('No hay movimientos para esta cuenta', 'Consulta Exitosa', wx.OK | wx.ICON_INFORMATION)
            else:
                movimientos_str = '\n'.join([f"{movimiento.description}: ${movimiento.amount:.2f}" for movimiento in movimientos])
                wx.MessageBox(f'Movimientos:\n{movimientos_str}', 'Consulta Exitosa', wx.OK | wx.ICON_INFORMATION)
        except NumeroTarjetaIncorrecto as e: 
            wx.MessageBox('Número de cuenta incorrecto', 'Error', wx.OK | wx.ICON_ERROR)

    def volver_menu_principal(self, event):
        self.Close()

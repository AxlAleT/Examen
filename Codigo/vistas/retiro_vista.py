import wx
from controladores.retiro_controlador import RetiroControlador
from excepciones.excepciones_tarjeta import NipIncorrecto
from excepciones.excepciones_tarjeta import SaldoInsuficiente
from excepciones.excepciones_billete import NoSePuedeDarMontoException

class Retiro(wx.Frame):
    def __init__(self, parent, numero_tarjeta=None):
        super().__init__(parent, title='Retiro de Efectivo', size=(300, 200))
        self.numero_tarjeta = numero_tarjeta
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_monto = wx.StaticText(panel, label='Monto a retirar:')
        self.text_monto = wx.TextCtrl(panel)
        hbox1.Add(label_monto, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_monto, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label_nip = wx.StaticText(panel, label='NIP:')
        self.text_nip = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        hbox2.Add(label_nip, 0, wx.ALL | wx.CENTER, 5)
        hbox2.Add(self.text_nip, 1, wx.ALL | wx.EXPAND, 5)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        button_retirar = wx.Button(panel, label='Retirar')
        button_retirar.Bind(wx.EVT_BUTTON, self.retirar_efectivo)
        hbox3.Add(button_retirar, 0, wx.ALL | wx.CENTER, 5)
        button_volver = wx.Button(panel, label='Volver al Menú Principal')
        button_volver.Bind(wx.EVT_BUTTON, self.volver_menu_principal)
        hbox3.Add(button_volver, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox3, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)

    def retirar_efectivo(self, event):
        montoString = self.text_monto.GetValue()
        nip = self.text_nip.GetValue()
        monto = int(montoString)
        try: 
            billetes = RetiroControlador.retirar(self.numero_tarjeta, monto, nip)
            self.Close()
            mostrarBilletes = MostrarBilletes(None, billetes=billetes)
            mostrarBilletes.Show()
        except NipIncorrecto as e: 
            wx.MessageBox('NIP incorrecto', 'Error', wx.OK | wx.ICON_ERROR)
        except SaldoInsuficiente as e:
            wx.MessageBox('Saldo insuficiente', 'Error', wx.OK | wx.ICON_ERROR)
        except NoSePuedeDarMontoException as e:
            wx.MessageBox('No hay billetes disponibles para esa cantidad', 'Error', wx.OK | wx.ICON_ERROR)

    def volver_menu_principal(self, event):
        self.Close() 
        

class MostrarBilletes(wx.Frame):
    def __init__(self, parent, billetes):
        super().__init__(parent, title='Mostrar Billetes', size=(300, 400))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Título del frame
        titulo = wx.StaticText(panel, label='Billetes y Cantidades')
        font = titulo.GetFont()
        font.PointSize += 4
        font = font.Bold()
        titulo.SetFont(font)
        vbox.Add(titulo, 0, wx.ALL | wx.CENTER, 10)

        # Imprimir denominación y cantidad
        for denominacion, cantidad in billetes:
            label = wx.StaticText(panel, label=f'Denominación: {denominacion}, Cantidad: {cantidad}')
            vbox.Add(label, 0, wx.ALL | wx.CENTER, 5)

        # Botón para cerrar el frame
        button_cerrar = wx.Button(panel, label='Cerrar')
        button_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_frame)
        vbox.Add(button_cerrar, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(vbox)
        self.Show()

    def cerrar_frame(self, event):
        self.Close()
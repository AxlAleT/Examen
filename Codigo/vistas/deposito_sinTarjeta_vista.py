import wx
from controladores.deposito_controlador import DepositoControlador
from excepciones.excepciones_tarjeta import NumeroTarjetaIncorrecto

class DepositoSinTarjeta(wx.Frame):
    """
      Clase para la interfaz de depósito de efectivo sin tarjeta.

    Esta clase representa la ventana de depósito de efectivo cuando no se tiene
    el número de tarjeta.

    Args:
        parent (wx.Window): La ventana principal de la aplicación.

    """
    def __init__(self, parent):
         """
          Inicializa la ventana de depósito de efectivo sin tarjeta.

        Args:
            parent (wx.Window): La ventana principal de la aplicación.

        """
        super().__init__(parent, title='Depósito de Efectivo', size=(300, 200))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_tarjeta = wx.StaticText(panel, label='Número de tarjeta:')
        self.text_tarjeta = wx.TextCtrl(panel)
        hbox1.Add(label_tarjeta, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_tarjeta, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label_monto = wx.StaticText(panel, label='Monto a depositar:')
        self.text_monto = wx.TextCtrl(panel)
        hbox2.Add(label_monto, 0, wx.ALL | wx.CENTER, 5)
        hbox2.Add(self.text_monto, 1, wx.ALL | wx.EXPAND, 5)

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
         """
          Método para realizar el depósito de efectivo.

        Este método se llama cuando se presiona el botón de depósito. Obtiene
        el número de tarjeta y el monto ingresados por el usuario, luego intenta
        realizar el depósito llamando al controlador correspondiente.

        Args:
            event: El evento que desencadenó la llamada al método.

        """
        num_tarjeta = self.text_tarjeta.GetValue()
        monto_string = self.text_monto.GetValue()

        try:
            DepositoControlador.depositar(num_tarjeta, monto_string)
            wx.MessageBox('Depósito realizado con éxito', 'Información', wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except NumeroTarjetaIncorrecto:
            wx.MessageBox('Número de tarjeta incorrecto', 'Error', wx.OK | wx.ICON_ERROR)
        except ValueError:
            wx.MessageBox('Monto inválido', 'Error', wx.OK | wx.ICON_ERROR)

    def volver_menu_principal(self, event):
        """
         Método para volver al menú principal.

        Este método se llama cuando se presiona el botón para volver al menú
        principal. Cierra la ventana de depósito de efectivo.

        Args:
            event: El evento que desencadenó la llamada al método.

        """
        self.Close()

import wx
from controladores.deposito_controlador import DepositoControlador
from excepciones.excepciones_tarjeta import NumeroTarjetaIncorrecto

class Deposito(wx.Frame):
        """Clase para la interfaz de depósito de efectivo.

    Esta clase representa la ventana de depósito de efectivo en la interfaz
    gráfica de usuario.

    Args:
        parent (wx.Window): La ventana principal de la aplicación.
        numero_tarjeta (int, optional): El número de tarjeta asociado al depósito.

    Attributes:
        numero_tarjeta (int): El número de tarjeta asociado al depósito.

    """

    def __init__(self, parent, numero_tarjeta=None):
         """Inicializa la ventana de depósito de efectivo.

        Args:
            parent (wx.Window): La ventana principal de la aplicación.
            numero_tarjeta (int, optional): El número de tarjeta asociado al depósito.

        """
        super().__init__(parent, title='Depósito de Efectivo', size=(300, 150))
        self.numero_tarjeta = numero_tarjeta
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_monto = wx.StaticText(panel, label='Monto a depositar:')
        self.text_monto = wx.TextCtrl(panel)
        hbox1.Add(label_monto, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_monto, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        button_depositar = wx.Button(panel, label='Depositar')
        button_depositar.Bind(wx.EVT_BUTTON, self.depositar_efectivo)
        hbox2.Add(button_depositar, 0, wx.ALL | wx.CENTER, 5)
        button_volver = wx.Button(panel, label='Volver al Menú Principal')
        button_volver.Bind(wx.EVT_BUTTON, self.volver_menu_principal)
        hbox2.Add(button_volver, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)

    def depositar_efectivo(self, event):
        """Método para realizar el depósito de efectivo.

        Este método se llama cuando se presiona el botón de depósito. Obtiene
        el monto y el NIP ingresados por el usuario, luego intenta realizar
        el depósito llamando al controlador correspondiente.

        Args:
            event: El evento que desencadenó la llamada al método.

        """
        monto_string = self.text_monto.GetValue()

        try:
            DepositoControlador.depositar(self.numero_tarjeta, monto_string)
            wx.MessageBox('Depósito realizado con éxito', 'Información', wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except NumeroTarjetaIncorrecto:
            wx.MessageBox('Número de tarjeta incorrecto', 'Error', wx.OK | wx.ICON_ERROR)
        except ValueError:
            wx.MessageBox('Monto inválido', 'Error', wx.OK | wx.ICON_ERROR)

    def volver_menu_principal(self, event):
            """Método para volver al menú principal.

        Este método se llama cuando se presiona el botón para volver al menú
        principal. Cierra la ventana de depósito de efectivo.

        Args:
            event: El evento que desencadenó la llamada al método.

        """
        self.Close()

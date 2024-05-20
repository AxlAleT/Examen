import wx
from controladores.saldosmov_controlador import ConsultaControlador
from excepciones.excepciones_tarjeta import NumeroTarjetaIncorrecto

class ConsultaSaldo(wx.Frame):
    """
    Clase que representa la ventana para consultar el saldo de una cuenta.

    Attributes:
        num_tarjeta (str): El número de tarjeta para la cual se consulta el saldo.
    """

    def __init__(self, parent, num_tarjeta):
        """
        Inicializa la ventana de consulta de saldo.

        Args:
            parent (wx.Window): La ventana principal o padre de esta ventana.
            num_tarjeta (str): El número de tarjeta para la cual se consulta el saldo.
        """
        super().__init__(parent, title='Consulta de Saldo', size=(300, 200))
        self.num_tarjeta = num_tarjeta
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_saldo = wx.StaticText(panel, label='Saldo Actual:')
        self.text_saldo = wx.StaticText(panel, label='')
        hbox1.Add(label_saldo, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_saldo, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        button_volver = wx.Button(panel, label='Volver al Menú Principal')
        button_volver.Bind(wx.EVT_BUTTON, self.volver_menu_principal)
        hbox2.Add(button_volver, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)

        self.consultar_saldo()

    def consultar_saldo(self):
        """
        Consulta el saldo de la cuenta asociada al número de tarjeta.
        """
        try:
            saldo = ConsultaControlador.consultar_saldo(self.num_tarjeta)
            self.text_saldo.SetLabel(f'${saldo:.2f}')
        except NumeroTarjetaIncorrecto:
            wx.MessageBox('Número de tarjeta incorrecto', 'Error', wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f'Error al consultar el saldo: {str(e)}', 'Error', wx.OK | wx.ICON_ERROR)

    def volver_menu_principal(self, event):
        """
        Cierra la ventana y vuelve al menú principal.

        Args:
            event: El evento que activa la función (en este caso, el clic en el botón).
        """
        self.Close()


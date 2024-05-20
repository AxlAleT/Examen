import wx
from controladores.saldosmov_controlador import ConsultaControlador
from excepciones.excepciones_tarjeta import NumeroTarjetaIncorrecto

class ConsultaSaldo(wx.Frame):
    """
    Clase que representa la ventana para consultar el saldo de una cuenta mediante el número de tarjeta.

    Attributes:
        parent (wx.Window): La ventana principal o padre de esta ventana.
        numero_tarjeta (str): El número de tarjeta asociado a la consulta.

    Methods:
        __init__(parent, numero_tarjeta): Inicializa la ventana de consulta de saldo.
        consultar_saldo(event): Realiza la consulta de saldo.
        volver_menu_principal(event): Cierra la ventana y vuelve al menú principal.
    """

    def __init__(self, parent, numero_tarjeta=None):
        """
        Inicializa la ventana de consulta de saldo.

        Args:
            parent (wx.Window): La ventana principal o padre de esta ventana.
            numero_tarjeta (str): El número de tarjeta asociado a la consulta.
        """
        super().__init__(parent, title='Consulta de Saldo', size=(300, 200))
        self.numero_tarjeta = numero_tarjeta
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_tarjeta = wx.StaticText(panel, label='Número de Tarjeta:')
        self.text_tarjeta = wx.TextCtrl(panel)
        hbox1.Add(label_tarjeta, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_tarjeta, 1, wx.ALL | wx.EXPAND, 5)

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
        """
        Realiza la consulta de saldo.

        Args:
            event: El evento que activa la función (en este caso, el clic en el botón).
        """
        num_tarjeta = self.text_tarjeta.GetValue()
        try:
            saldo = ConsultaControlador.consultar_saldo(num_tarjeta)
            self.mostrar_saldo(saldo)
        except NumeroTarjetaIncorrecto as e:
            wx.MessageBox('Número de tarjeta incorrecto', 'Error', wx.OK | wx.ICON_ERROR)

    def mostrar_saldo(self, saldo):
        """
        Muestra el saldo en una ventana emergente.

        Args:
            saldo (float): El saldo a mostrar.
        """
        wx.MessageBox(f'Saldo Actual: ${saldo:.2f}', 'Saldo', wx.OK | wx.ICON_INFORMATION)

    def volver_menu_principal(self, event):
        """
        Cierra la ventana y vuelve al menú principal.

        Args:
            event: El evento que activa la función (en este caso, el clic en el botón).
        """
        self.Close()

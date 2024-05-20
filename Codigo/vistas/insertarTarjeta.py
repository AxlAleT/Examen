import wx
from vistas.menuCompleto import MenuCompleto
from controladores.tarjeta_controlador import TarjetaControlador
from excepciones.excepciones_tarjeta import NipIncorrecto

class InsertarTarjeta(wx.Frame):
    """Clase para la interfaz de inserción de tarjeta.

    Esta clase representa la ventana donde el usuario puede insertar el número de tarjeta
    y el NIP para acceder al menú completo.

    Args:
        parent (wx.Window): La ventana principal de la aplicación.

    """
    def __init__(self, parent):
        """Inicializa la ventana de inserción de tarjeta.

        Args:
            parent (wx.Window): La ventana principal de la aplicación.

        """
        super().__init__(parent, title='Insertar Tarjeta', size=(300, 200))
        self.parent = parent
        self.numero_tarjeta = None  # Variable para almacenar el número de tarjeta
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_tarjeta = wx.StaticText(panel, label='Número de Tarjeta:')
        self.text_tarjeta = wx.TextCtrl(panel)
        hbox1.Add(label_tarjeta, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_tarjeta, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label_nip = wx.StaticText(panel, label='NIP:')
        self.text_nip = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        hbox2.Add(label_nip, 0, wx.ALL | wx.CENTER, 5)
        hbox2.Add(self.text_nip, 1, wx.ALL | wx.EXPAND, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)

        button_validar = wx.Button(panel, label='Validar')
        button_validar.Bind(wx.EVT_BUTTON, self.validar_nip)
        vbox.Add(button_validar, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(vbox)

    def validar_nip(self, event):
        """Método para validar el NIP ingresado.

        Este método se llama cuando se presiona el botón de validar. Obtiene el número de
        tarjeta y el NIP ingresados por el usuario, luego intenta validar el NIP llamando
        al controlador correspondiente.

        Args:
            event: El evento que desencadenó la llamada al método.

        """
        numero_tarjeta = self.text_tarjeta.GetValue()
        nip = self.text_nip.GetValue()
        tarjetaControlador = TarjetaControlador()

        if not tarjetaControlador.validar_numero_tarjeta(numero_tarjeta):
            wx.MessageBox('Número de tarjeta incorrecto', 'Error', wx.OK | wx.ICON_ERROR)
            return

        try:
            tarjetaControlador.validar_nip(numero_tarjeta, nip)
            wx.MessageBox('NIP correcto', 'Éxito', wx.OK | wx.ICON_INFORMATION)
            self.Close()
            self.parent.Close()
            # Aquí pasamos el número de tarjeta al Menú Completo
            menu_completo_frame = MenuCompleto(None, numero_tarjeta=numero_tarjeta)
            menu_completo_frame.Show()
        except NipIncorrecto as e:
            wx.MessageBox('NIP incorrecto', 'Error', wx.OK | wx.ICON_ERROR)

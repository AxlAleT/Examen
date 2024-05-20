import wx
from controladores.pago_TarjetaCredito_controlador import PagoTarjetaCreditoControlador
from excepciones.excepciones_tarjeta import NumeroTarjetaIncorrecto

class PagoTarjetaCredito(wx.Frame):
    """
    Clase que representa la ventana para realizar un pago a una tarjeta de crédito en un cajero automático.

    Attributes:
        parent (wx.Window): La ventana principal o padre de esta ventana.
        numero_tarjeta (str): El número de tarjeta de crédito a la que se realizará el pago.

    Methods:
        __init__(parent, numero_tarjeta): Inicializa la ventana de pago a tarjeta de crédito.
        pagar_tarjeta(event): Realiza el pago a la tarjeta de crédito.
        volver_menu_principal(event): Cierra la ventana y vuelve al menú principal.
    """

    def __init__(self, parent, numero_tarjeta):
        """
        Inicializa la ventana de pago a tarjeta de crédito.

        Args:
            parent (wx.Window): La ventana principal o padre de esta ventana.
            numero_tarjeta (str): El número de tarjeta de crédito a la que se realizará el pago.
        """
        super().__init__(parent, title='Pago a Tarjeta de Crédito', size=(300, 150))
        self.numero_tarjeta = numero_tarjeta
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_monto = wx.StaticText(panel, label='Monto a pagar:')
        self.text_monto = wx.TextCtrl(panel)
        hbox1.Add(label_monto, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(self.text_monto, 1, wx.ALL | wx.EXPAND, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        button_pagar = wx.Button(panel, label='Pagar')
        button_pagar.Bind(wx.EVT_BUTTON, self.pagar_tarjeta)
        hbox2.Add(button_pagar, 0, wx.ALL | wx.CENTER, 5)
        button_volver = wx.Button(panel, label='Volver al Menú Principal')
        button_volver.Bind(wx.EVT_BUTTON, self.volver_menu_principal)
        hbox2.Add(button_volver, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(hbox1, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(hbox2, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)

    def pagar_tarjeta(self, event):
        """
        Realiza el pago a la tarjeta de crédito.

        Args:
            event: El evento que activa la función (en este caso, el clic en el botón).
        """
        monto_string = self.text_monto.GetValue()

        try:
            PagoTarjetaCreditoControlador.pagar_tarjeta_credito(self.numero_tarjeta, monto_string)
            wx.MessageBox('Pago realizado con éxito', 'Información', wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except NumeroTarjetaIncorrecto:
            wx.MessageBox('Número de tarjeta incorrecto', 'Error', wx.OK | wx.ICON_ERROR)
        except ValueError:
            wx.MessageBox('Monto inválido', 'Error', wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f'Error inesperado: {str(e)}', 'Error', wx.OK | wx.ICON_ERROR)

    def volver_menu_principal(self, event):
        """
        Cierra la ventana y vuelve al menú principal.

        Args:
            event: El evento que activa la función (en este caso, el clic en el botón).
        """
        self.Close()

# main function to run the application
if __name__ == "__main__":
    app = wx.App(False)
    frame = PagoTarjetaCredito(None, numero_tarjeta='1234567890123456')
    frame.Show()
    app.MainLoop()

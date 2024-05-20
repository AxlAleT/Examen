import wx
from controladores.Servicio_controlador import ServicioControlador

class SeleccionarServicio(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title='Seleccionar Servicio', size=(400, 300))
        self.parent = parent  # Guardar el parent para usarlo más tarde
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        label_titulo = wx.StaticText(panel, label='Seleccione un Servicio')
        font = label_titulo.GetFont()
        font.PointSize += 4
        font = font.Bold()
        label_titulo.SetFont(font)
        vbox.Add(label_titulo, 0, wx.ALL | wx.CENTER, 10)

        self.lista_servicios = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.lista_servicios.InsertColumn(0, 'Nombre del Servicio', width=200)
        self.lista_servicios.InsertColumn(1, 'Número de Convenio', width=150)

        servicios = ServicioControlador.obtener_servicios()
        for idx, (nombre, convenio) in enumerate(servicios):
            self.lista_servicios.InsertItem(idx, nombre)
            self.lista_servicios.SetItem(idx, 1, str(convenio))

        self.lista_servicios.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)

        vbox.Add(self.lista_servicios, 1, wx.ALL | wx.EXPAND, 10)

        button_cerrar = wx.Button(panel, label='Cerrar')
        button_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_frame)
        vbox.Add(button_cerrar, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(vbox)
        self.Show()

    def on_item_selected(self, event):
        item = event.GetItem()
        nombre = item.GetText()
        convenio = self.lista_servicios.GetItem(item.GetId(), 1).GetText()
        num_convenio = int(convenio)
        print(f"Nombre del Servicio: {nombre}, Número de Convenio: {convenio}")
        from vistas.pago_Servicio_sin_tarjeta_vista import PagoServicioSinTarjeta

        # Crear el nuevo frame antes de cerrar el actual
        pagoServicioSinTarjeta = PagoServicioSinTarjeta(parent=self.parent, num_convenio=num_convenio)
        self.Close()
        pagoServicioSinTarjeta.Show()

    def cerrar_frame(self, event):
        self.Close()


# seleccionar_servicio_para_tarjeta.py

class SeleccionarServicioParaTarjeta(wx.Frame):
    def __init__(self, parent, num_tarjeta):
        super().__init__(parent, title='Seleccionar Servicio', size=(400, 300))
        self.parent = parent
        self.num_tarjeta = num_tarjeta
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        label_titulo = wx.StaticText(panel, label='Seleccione un Servicio')
        font = label_titulo.GetFont()
        font.PointSize += 4
        font = font.Bold()
        label_titulo.SetFont(font)
        vbox.Add(label_titulo, 0, wx.ALL | wx.CENTER, 10)

        self.lista_servicios = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.lista_servicios.InsertColumn(0, 'Nombre del Servicio', width=200)
        self.lista_servicios.InsertColumn(1, 'Número de Convenio', width=150)

        servicios = ServicioControlador.obtener_servicios()
        for idx, (nombre, convenio) in enumerate(servicios):
            self.lista_servicios.InsertItem(idx, nombre)
            self.lista_servicios.SetItem(idx, 1, str(convenio))

        self.lista_servicios.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)

        vbox.Add(self.lista_servicios, 1, wx.ALL | wx.EXPAND, 10)

        button_cerrar = wx.Button(panel, label='Cerrar')
        button_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_frame)
        vbox.Add(button_cerrar, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(vbox)
        self.Show()

    def on_item_selected(self, event):
        item = self.lista_servicios.GetFirstSelected()
        if item == -1:
            wx.MessageBox('Por favor, seleccione un servicio', 'Info', wx.OK | wx.ICON_INFORMATION)
            return
        
        nombre = self.lista_servicios.GetItemText(item, 0)
        convenio = self.lista_servicios.GetItemText(item, 1)
        num_convenio = int(convenio)
        print(f"Nombre del Servicio: {nombre}, Número de Convenio: {convenio}")

        from vistas.pago_Servicio_tarjeta_vista import PagoServicioConTarjeta

        pagoServicioConTarjeta = PagoServicioConTarjeta(parent=self.parent, num_tarjeta=self.num_tarjeta, num_convenio=num_convenio)
        self.Close()
        pagoServicioConTarjeta.Show()

    def cerrar_frame(self, event):
        self.Close()

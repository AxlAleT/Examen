import wx
from vistas.menuPrincipal import MenuPrincipal

if __name__ == '__main__':
    app = wx.App(False)
    while(1):
        frame = MenuPrincipal()
        app.MainLoop()

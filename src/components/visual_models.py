
if __name__ == '__main__':
    from base_models import *
    print('Visual models definition.')
else:
    from components.base_models import *


class PMenuCommand(PMenuBase):

    def __init__(self, title='MenuCommand', accelerator=None, image=None, cmd=None) -> None:
        super().__init__(title, accelerator, image, cmd)


class PMenuItem(PMenuBase):

    def __init__(self, title='MenuItem', accelerator=None, image=None, cmd=None) -> None:
        super().__init__(title, accelerator, image, cmd)


class PMenuBar(PMenuBase):

    def __init__(self):
        super().__init__(title='MainMenuBar')


class PPanel(Frame, PWidget):

    def __init__(self):

        Frame.__init__(self, None)
        PWidget.__init__(self, self.master, self.widgetName)

        self.Width = 10  # Default width
        self.Height = 20  # Default height
        self.Background = None  # Default background

    def add(self, widget: PWidget):
        widget.master = self
        widget.place(x=widget.x, y=widget.y,
                     width=widget.Width, height=widget.Height)


class PFrame(Frame, PWidget):

    @property
    def MenuBar(self):
        return self._menuBar

    @MenuBar.setter
    def MenuBar(self, value: PMenuBar):
        if not isinstance(value, PMenuBar):
            raise TypeError('Has to be PMenuBar type')

        self._menuBar = value
        self._master.configure(menu=self._menuBar.InternalMenu)

    @property
    def Title(self):
        return self._title

    @Title.setter
    def Title(self, value: str):
        self._title = str(value)
        self._master.title(self._title)

    def __init__(self) -> None:
        self._master = Tk()

        Frame.__init__(self, self._master)
        PWidget.__init__(self, self._master, self.widgetName)

        self.Title = "Main Window"
        self.Width = 150  # Default width
        self.Height = 0  # Default height
        self.Background = "white"  # Default background

        # see: https://recursospython.com/guias-y-manuales/barra-de-menu-tkinter/
        self.MenuBar = PMenuBar()

        self.create_widgets()  # InitComponents

    def create_widgets(self):
        fileMenu = PMenuItem(title='Archivo')


        fileMenu.add(PMenuCommand(
            title='Abrir',
            cmd=lambda: print('Abriendo...')
        ))

        fileMenu.add(PMenuCommand(
            title='Guardar',
            cmd=lambda: print('Guardando...')
        ))

        self.MenuBar.add(fileMenu)

    def add(self, widget: PWidget):
        widget.master = self
        widget.place(x=widget.x, y=widget.y,
                     width=widget.Width, height=widget.Height)

    def show(self):
        self.pack(fill='both')
        self.mainloop()

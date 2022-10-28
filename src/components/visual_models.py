
if __name__ == '__main__':
    from base_models import *
    print('Visual models definition.')
else:
    from components.base_models import *


class PMenuSeparator():

    @property
    def Background(self):
        return self._bg

    @Background.setter
    def Background(self, value: str):
        self._bg = str(value)

    def __init__(self, background=None) -> None:
        self.Background = background


class PMenuCommand(PMenuBase):

    def __init__(self, title='MenuCommand', accelerator='', image=None, cmd=None) -> None:
        super().__init__(title, accelerator, image, cmd)


class PMenuItem(PMenuBase):

    def __init__(self, title='MenuItem', accelerator='', image=None, cmd=None) -> None:
        super().__init__(title, accelerator, image, cmd)


class PMenuBar(PMenuBase):

    def __init__(self):
        super().__init__(title='MainMenuBar')

# Hacer PLabel, PTextBox, PButton


class PLabel(Label, PWidget):
    pass


class PPanel(Frame, PWidget):

    @PWidget.Width.setter
    def Width(self, value: 'str | float'):
        self.Width = value
        self.configure(width=value)

    @PWidget.Height.setter
    def Height(self, value: 'str | float'):
        self.Height = value
        self.configure(height=value)

    @PWidget.Background.setter
    def Background(self, value: str):
        self.Background = value
        self.configure(background=value)

    def __init__(self, x=0, y=0, width=20, height=20, background=None):

        Frame.__init__(self, None)
        PWidget.__init__(self, self.master, self.widgetName)

        self.x = x                      # Default x position
        self.y = y                      # Default y position
        self.Width = width              # Default width
        self.Height = height            # Default height
        self.Background = background    # Default background


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

    @PWidget.Width.setter
    def Width(self, value: 'str | float'):
        self.Width = value
        self.configure(width=value)

    @PWidget.Height.setter
    def Height(self, value: 'str | float'):
        self.Height = value
        self.configure(height=value)

    @PWidget.Background.setter
    def Background(self, value: str):
        self.Background = value
        self.configure(background=value)

    @property
    def Title(self):
        return self._title

    @Title.setter
    def Title(self, value: str):
        self._title = str(value)
        self._master.title(self._title)

    def __init__(self, title='Main Window', width=150, height=0, background='white') -> None:
        self._master = Tk()

        Frame.__init__(self, self._master)
        PWidget.__init__(self, self._master, self.widgetName)

        self.Title = title
        self.Width = width              # Default width
        self.Height = height            # Default height
        self.Background = background    # Default background

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

        panel = PPanel(x=50, y=50, width=50, height=100)

        self.add(panel)

        lblTest = Label(self, text='Test')
        lblTest.place(x=100, y=100)

    def show(self):
        self.pack(fill='both')
        self.mainloop()

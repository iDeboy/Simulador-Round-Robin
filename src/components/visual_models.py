
if __name__ == '__main__':
    from base_models import *
    print('Visual models definition.')
else:
    from components.base_models import *

class PMenuBar(tk.Menu):
    
    def __init__(self):
        super().__init__(tearoff=False)

    def addMenu(self, menu):
        pass

    def addCommand(self):
        pass

class PPanel(tk.Frame, PWidget):

    def __init__(self):

        tk.Frame.__init__(self, None)
        PWidget.__init__(self, self.master, self.widgetName)

        self.Width = 10  # Default width
        self.Height = 20  # Default height
        self.Background = None  # Default background

    def add(self, widget: PWidget):
        widget.master = self
        widget.place(x=widget.x, y=widget.y,
                     width=widget.Width, height=widget.Height)

class PFrame(tk.Frame, PWidget):

    @property
    def MenuBar(self):
        return self._menuBar

    @MenuBar.setter
    def MenuBar(self, value: PMenuBar):
        if not isinstance(value, PMenuBar): raise TypeError('Has to be PMenuBar type')

        self._menuBar = value
        self._master.configure(menu=self._menuBar)

    @property
    def Title(self):
        return self._title

    @Title.setter
    def Title(self, value: str):
        self._title = str(value)
        self._master.title(self._title)

    def __init__(self) -> None:
        self._master = Tk()

        tk.Frame.__init__(self, self._master)
        PWidget.__init__(self, self._master, self.widgetName)

        self.Title = "Simulación"
        self.Width = 150  # Default width
        self.Height = 0  # Default height
        self.Background = "white"  # Default background

        self.MenuBar = PMenuBar()
        # see: https://recursospython.com/guias-y-manuales/barra-de-menu-tkinter/
        fileMenu = tk.Menu(tearoff=False)

        self.MenuBar.add_command(label='test', accelerator='Ctrl+T')

        fileMenu.add_command(
            label='Abrir',
            accelerator='Ctrl+O',
            command = lambda: print('Abriendo...')
        )

        fileMenu.add_command(
            label='Guardar',
            accelerator='Ctrl+S',
            command = lambda: print('Guardando...')
        )

        self.MenuBar.add_cascade(label='Archivo', menu=fileMenu)

        self.create_widgets()  # InitComponents

    def create_widgets(self):
        pass

    def add(self, widget: PWidget):
        widget.master = self
        widget.place(x=widget.x, y=widget.y,
                     width=widget.Width, height=widget.Height)

    def show(self):
        self.pack(fill='both')
        self.mainloop()
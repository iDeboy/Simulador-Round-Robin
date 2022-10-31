
from tkinter.ttk import Treeview


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
        self._bg = value

    def __init__(self, background='black') -> None:
        self.Background = background


class PMenuCommand(PMenuBase):

    def __init__(self, title='MenuCommand', accelerator='', image=None, cmd=None) -> None:
        super().__init__(title, accelerator, image, cmd)


class PMenuItem(PMenuBase):

    def __init__(self, title='MenuItem', accelerator='', image=None, cmd=None) -> None:
        super().__init__(title, accelerator, image, cmd)


class PDataGridColumn():
    
    @property
    def Id(self):
        return self._id

    @Id.setter
    def Id(self, value: str):
        self._id = value

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, value: str):
        self._name = value

    @property
    def Values(self):
        return self._values

    @property
    def Width(self):
        return self._width

    @Width.setter
    def Width(self, value: int):
        self._width = int(value)

    @property
    def MinWidth(self):
        return self._minwidth

    @MinWidth.setter
    def MinWidth(self, value: int):
        self._minwidth = int(value)

    def __init__(self, id: str, name: str, width = 80, minwidth = 30) -> None:
        
        self._values = list()
        self.Id = id
        self.Name = name
        self.Width = width
        self.MinWidth = minwidth

    def __str__(self) -> str:
        return '{\n'+f'\tId: \'{self.Id}\'\n\tName: \'{self.Name}\'\n\tValues: {self.Values}\n\tWidth: {self.Width}\n\tMinWidth: {self.MinWidth}' + '\n}'

class PDataGrid(Treeview, PWidget):

    @property
    def Columns(self) -> dict:
        return self._columns

    def __init__(self, x=0, y=0):
        Treeview.__init__(self)
        PWidget.__init__(self, self.master, self.widgetName)

        self._columns = dict()
        self._index = 0

        self.x = x
        self.y = y

    def add_column(self, name: str, width = 80, minwidth = 30):
        col = PDataGridColumn(f'#{self._index}', str(name), width, minwidth)
        self.Columns[col.Id] = col
        self._index += 1

        keys = list(self.Columns)
        keys.remove('#0')

        self.configure(columns=keys)

    #Crear clase PDataGridRow
    def add_row(self, values: list):
        pass
        

class PMenuBar(PMenuBase):

    def __init__(self):
        super().__init__(title='MainMenuBar')


class PButton(Button, PWidget):

    def __init__(self, title='Button', x=0, y=0, background=None, foreground='black', justify='left', borderwidth=3, relief='groove', cmd=None):
        Button.__init__(self, None)
        PWidget.__init__(self, self.master, self.widgetName)

        self.Title = title
        self.x = x
        self.y = y
        self.Background = background
        self.Foreground = foreground
        self.Justify = justify
        self.BorderWidth = borderwidth
        self.Relief = relief
        self.Cursor = 'hand2'
        self.Command = cmd


class PTextBox(Entry, PWidget):

    def __init__(self, title='', x=0, y=0, background=None, foreground='black', justify='left', width=30, borderwidth=3, relief='groove'):
        Entry.__init__(self, None)
        PWidget.__init__(self, self.master, self.widgetName)

        self.Title = title
        self.x = x
        self.y = y
        self.Background = background
        self.Foreground = foreground
        self.Justify = justify
        self.Width = width
        self.BorderWidth = borderwidth
        self.Relief = relief

    def clear(self):
        self.Title = ''


class PLabel(Label, PWidget):

    def __init__(self, title='Label', x=0, y=0, background=None, foreground='black', justify='left'):
        Label.__init__(self, None)
        PWidget.__init__(self, self.master, self.widgetName)

        self.Title = title
        self.x = x
        self.y = y
        self.Background = background
        self.Foreground = foreground
        self.Justify = justify


class PPanel(Frame, PWidget):

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

    @property
    def Title(self):
        return super().Title

    @Title.setter
    def Title(self, value: str):
        self._title = value
        self._master.title(self._title)

    def __init__(self, title='Main Window', width=150, height=0, background='white') -> None:
        self._master = Tk()
        self._master.resizable(False, False)
        Frame.__init__(self, self._master)
        PWidget.__init__(self, self._master, self.widgetName)

        self.Title = title
        self.Width = width              # Default width
        self.Height = height            # Default height
        self.Background = background    # Default background

        # see: https://recursospython.com/guias-y-manuales/barra-de-menu-tkinter/
        self.MenuBar = PMenuBar()

        # self.create_widgets()  # InitComponents

    def test_create_widgets(self):
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

        lblTest = PLabel(title='Test', x=500, y=100,
                         foreground='red', background=self.Background)

        txtBoxTest = PTextBox(x=100, y=100)

        btnTest = PButton(title='Limpiar', x=100, y=150)

        self.add(btnTest)

        self.add(txtBoxTest)

        self.add(lblTest)

        self.add(panel)

    def show(self):
        self.pack(fill=BOTH, expand=TRUE)
        self.mainloop()

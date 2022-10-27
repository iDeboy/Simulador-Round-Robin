
from multiprocessing.forkserver import write_signed
import tkinter as tk
from tkinter import Misc, Tk
from typing_extensions import TypeAlias

_ScreenUnits: TypeAlias = 'str | float'
_Color: TypeAlias = str

class PWidget(tk.Widget):

    def __init__(self, master: 'Misc | None', classname: str) -> None:

        tk.Widget.__init__(self, master, classname)
        
        self.x = 0
        self.y = 0
        self.Width = 0 # Default width
        self.Height = 0 # Default height
        self.Background = None # Default background

    #Properties
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: _ScreenUnits) -> None:
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: _ScreenUnits) -> None:
        self._y = value

    @property
    def Width(self):
        return self._width

    @Width.setter
    def Width(self, value: _ScreenUnits) -> None:
        self['width'] = self._width = value

    @property
    def Height(self):
        return self._width

    @Height.setter
    def Height(self, value: _ScreenUnits) -> None:
        self['height'] = self._height = value

    @property
    def Background(self):
        return self._bg
    
    @Background.setter
    def Background(self, value: _Color):
        self['bg'] = self._bg = value

class PFrame(tk.Frame, PWidget):

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
        self.Width = 150 # Default width
        self.Height = 0 # Default height
        self.Background = "white" # Default background
        
        self.create_widgets() #InitComponents

    def create_widgets(self):
        pass

    def add(self, widget: PWidget):
        widget.master = self
        widget.place(x=widget.x, y=widget.y, width=widget.Width, height=widget.Height)

    def show(self):
        self.pack(fill='both')
        self.mainloop()

class PPanel(tk.Frame, PWidget):

    def __init__(self):

        tk.Frame.__init__(self, None)
        PWidget.__init__(self, self.master, self.widgetName)
        
        self.Width = 10 # Default width
        self.Height = 20 # Default height
        self.Background = None # Default background
    
    def add(self, widget: PWidget):
        widget.master = self
        widget.place(x=widget.x, y=widget.y, width=widget.Width, height=widget.Height)

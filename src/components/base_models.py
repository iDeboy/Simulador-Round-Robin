import tkinter as tk
from tkinter import Tk

if __name__ == '__main__':
    print('Base components definition.')

class PWidget(tk.Widget):

    def __init__(self, master: 'tk.Misc | None', classname: str) -> None:

        tk.Widget.__init__(self, master, classname)

        self.x = 0
        self.y = 0
        self.Width = 0  # Default width
        self.Height = 0  # Default height
        self.Background = None  # Default background

    # Properties
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: 'str | float') -> None:
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: 'str | float') -> None:
        self._y = value

    @property
    def Width(self):
        return self._width

    @Width.setter
    def Width(self, value: 'str | float') -> None:
        self['width'] = self._width = value

    @property
    def Height(self):
        return self._width

    @Height.setter
    def Height(self, value: 'str | float') -> None:
        self['height'] = self._height = value

    @property
    def Background(self):
        return self._bg

    @Background.setter
    def Background(self, value: str):
        self['bg'] = self._bg = value

class PMenuBase(tk.Widget):

    def __init__(self, master: 'tk.Misc | None', classname: str) -> None:

        tk.Widget.__init__(self, master, classname)

    @property
    def Title(self):
        return self._title
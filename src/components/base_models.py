from tkinter import *
from typing import Callable

if __name__ == '__main__':
    import visual_models as Visuals
    print('Base components definition.')
else:
    import components.visual_models as Visuals

class PWidget(Widget):

    def __init__(self, master: 'tk.Misc | None', classname: str) -> None:

        Widget.__init__(self, master, classname)

        self.x = 0              # Default x position
        self.y = 0              # Default t position
        self.Width = 0          # Default width
        self.Height = 0         # Default height
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

class PMenuBase:

    @property
    def InternalMenu(self):
        return self._internalMenu

    def __init__(self, title = 'Menu', accelerator = None, image = None, cmd = None) -> None:
        self._internalMenu = Menu(tearoff=False)
        self.Title = title
        self.Accelerator = accelerator
        self.Image = image
        self.Command = cmd

    def add(self, menu) -> None:

        if isinstance(menu, Visuals.PMenuItem):
            return self.InternalMenu.add_cascade(menu=menu.InternalMenu, label=menu.Title, accelerator=menu.Accelerator, image=menu.Image, command=menu.Command)
        elif isinstance(menu, Visuals.PMenuCommand):
            return self.InternalMenu.add_command(label=menu.Title, accelerator=menu.Accelerator, image=menu.Image, command=menu.Command)

        raise TypeError('Type not supported.')
        

    @property
    def Title(self):
        return self._title

    @Title.setter
    def Title(self, value: str):
        self._title = str(value)

    @property
    def Accelerator(self):
        return self._accelerator

    @Accelerator.setter
    def Accelerator(self, value: str):
        self._accelerator = str(value)

    @property
    def Image(self):
        return self._image

    @Image.setter
    def Image(self, value: 'str | Image'):
        self._image = value

    @property
    def Command(self):
        return self._command

    @Command.setter
    def Command(self, value: 'Callable[[], object] | str'):
        self._command = value

    """
    accelerator         <-      self.Accelerator
    activebackground
    activeforeground
    background
    bitmap
    columnbreak
    command             <-      self.Command
    compound
    font
    foreground
    hidemargin
    image               <-      self.Image
    label               <-      self.Title
    menu                <-      self.InternalMenu
    state
    underline
    """
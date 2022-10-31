from math import fabs
from tkinter import *
from typing import Callable, Literal

if __name__ == '__main__':
    import visual_models as Visuals
    print('Base components definition.')
else:
    import components.visual_models as Visuals


class PWidget(Widget):

    def __init__(self, master: 'Misc | None', classname: str) -> None:

        Widget.__init__(self, master, classname)

        self.x = 0              # Default x position
        self.y = 0              # Default t position
        self.Width = 0          # Default width
        self.Height = 0         # Default height
        self.Background = None  # Default background
        self.Foreground = 'black'
        self.Title = 'PWidget'
        self.BorderWidth = 0
        self.Relief = GROOVE
        self.Command = None
        self.State = NORMAL

    def add(self, widget):

        if not isinstance(widget, PWidget):
            raise TypeError('Only PWidget type allowed.')

        widget.master = self

        widget.place(x=widget.x, y=widget.y)

    def has_resource(self, resource_name: str) -> bool:
        try:
            self[resource_name]
            return True
        except TclError:
            pass

        return False

    def set_resource(self, resource_name: str, value):

        if self.has_resource(resource_name):
            self[resource_name] = value

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
        self._width = value
        self.set_resource('width', value)

    @property
    def Height(self):
        return self._height

    @Height.setter
    def Height(self, value: 'str | float') -> None:
        self._height = value
        self.set_resource('height', value)

    @property
    def Background(self):
        return self._bg

    @Background.setter
    def Background(self, value: str):
        self._bg = value
        self.set_resource('background', value)

    @property
    def Foreground(self):
        return self._fg

    @Foreground.setter
    def Foreground(self, value: str):
        self._fg = value
        self.set_resource('foreground', value)

    @property
    def Title(self):
        return self._title.get()

    @Title.setter
    def Title(self, value: str):
        self._title = Variable(value=value)

        self.set_resource('text', value)
        self.set_resource('textvariable', self._title)

    @property
    def Justify(self):
        return self._justify

    @Justify.setter
    def Justify(self, value: Literal['normal', 'active', 'disabled']):
        self._justify = value
        self.set_resource('justify', value)

    @property
    def BorderWidth(self):
        return self._borderwidth

    @BorderWidth.setter
    def BorderWidth(self, value: 'str | float'):
        self._borderwidth = value
        self.set_resource('borderwidth', value)

    @property
    def Relief(self):
        return self._relief

    @Relief.setter
    def Relief(self, value: Literal['raised', 'sunken', 'flat', 'ridge', 'solid', 'groove']):
        self._relief = value
        self.set_resource('relief', value)

    @property
    def Command(self):
        return self._cmd

    @Command.setter
    def Command(self, value: 'str | Callable[[]]'):
        self._cmd = value
        self.set_resource('command', value)

    @property
    def Cursor(self):
        return self._cursor

    @Cursor.setter
    def Cursor(self, value: str):
        self._cursor = value
        self.set_resource('cursor', value)

    @property
    def State(self):
        return self._state

    @State.setter
    def State(self, value: Literal["normal", "disabled", "readonly"]):
        self._state = value
        self.set_resource('state', value)

class PMenuBase():

    @property
    def InternalMenu(self):
        return self._internalMenu

    def __init__(self, title='Menu', accelerator='', image=None, cmd=None, state = NORMAL) -> None:
        self._internalMenu = Menu(tearoff=False)
        self.Title = title
        self.Accelerator = accelerator
        self.Image = image
        self.Command = cmd
        self.State = state

    def add(self, menu) -> None:

        if isinstance(menu, Visuals.PMenuItem):
            return self.InternalMenu.add_cascade(menu=menu.InternalMenu, label=menu.Title, accelerator=menu.Accelerator, image=menu.Image, command=menu.Command, state=menu.State)
        elif isinstance(menu, Visuals.PMenuCommand):
            return self.InternalMenu.add_command(label=menu.Title, accelerator=menu.Accelerator, image=menu.Image, command=menu.Command, state=menu.State)
        elif isinstance(menu, Visuals.PMenuSeparator):
            return self.InternalMenu.add_separator(menu.Background)

        raise TypeError('Type not supported.')

    @property
    def State(self):
        return self._state

    @State.setter
    def State(self, value: Literal["normal", "disabled", "readonly"]):
        self._state = value

    @property
    def Title(self):
        return self._title

    @Title.setter
    def Title(self, value: str):
        self._title = value

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

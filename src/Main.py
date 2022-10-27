from time import sleep
from tkinter import *
from Components.MainFrame import Frame

class Main:
    def __init__(self) -> None:
        root = Tk()

        frame = Frame(root)

        root.mainloop()

Main()
from tkinter import Tk, ttk, Event, Menu, FALSE


class Frame:

    def __init__(self, root: Tk) -> None:

        self.__width = int()
        self.__height = int()
        self.__x = int()
        self.__y = int()
        self.__title = str()

        self.__root = root

        self.Width = 1000
        self.Height = 700

        self.Title = "Simulación"

        root.bind('<Configure>', self.onResize)
        
        screen_width_middle = root.winfo_screenwidth() // 2
        screen_height_middle = root.winfo_screenheight() // 2

        frame_width_middle = self.Width // 2
        frame_height_middle = self.Height // 2

        self.x = screen_width_middle - frame_width_middle
        self.y = screen_height_middle - frame_height_middle
        
        root.configure(background="skyblue3")
        root.geometry(f'{self.Width}x{self.Height}+{self.x}+{self.y}')

        root.option_add('*tearOff', FALSE)
        menubar = Menu(root)
        menu_file = Menu(menubar)
        menu_edit = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_edit, label='Edit')

        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        root['menu'] = menubar
        #frame = InternalFrame(root, bg="skyblue3", width=self.Width, height=self.Height)
        #frame.pack()

    def onResize(self, event: Event):
        self.Height = event.height
        self.Width = event.width
        self.x = event.x
        self.y = event.y

    @property
    def Width(self) -> int:
        return self.__width

    @Width.setter
    def Width(self, value: int) -> None:

        if not isinstance(value, int):
            raise TypeError('Width has to be int')

        if value < 0:
            raise ValueError('Width has to be greater or equal than 0')

        self.__width = value

    @property
    def Height(self) -> int:
        return self.__height

    @Height.setter
    def Height(self, value: int) -> None:

        if not isinstance(value, int):
            raise TypeError('Height has to be int')

        if value < 0:
            raise ValueError('Height has to be greater or equal than 0')

        self.__height = value

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int) -> None:

        if not isinstance(value, int):
            raise TypeError('x has to be int')

        self.__x = value

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int) -> None:

        if not isinstance(value, int):
            raise TypeError('y has to be int')

        self.__y = value

    @property
    def Title(self) -> str:
        return self.__title

    @Title.setter
    def Title(self, value: str):
        self.__title = str(value)
        self.__root.title(self.__title)

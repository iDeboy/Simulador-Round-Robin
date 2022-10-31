
from tkinter.ttk import Treeview
from components.visual_models import *


class RoundRobin(PFrame):
    def __init__(self):
        super().__init__('Simulador', 800, 600)

        self.create_widgets()

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

        # Label para la aprte de agregar procesos
        self.add(PLabel(title='Agregar procesos:', x=200,
                 y=50, background=self.Background))

        # Label para el TextBox nombre del proceso
        self.add(PLabel(title='Nombre:', x=200,
                 y=100, background=self.Background))
        self.txtBoxNombreProc = PTextBox(x=200, y=130, width=15)
        self.add(self.txtBoxNombreProc)

        # Label para el TextBox tiempo del proceso
        self.add(PLabel(title='Tiempo:', x=350,
                 y=100, background=self.Background))

        self.txtBoxTiempoProc = PTextBox(x=350, y=130, width=15)
        self.add(self.txtBoxTiempoProc)

        self.lblErrorProc = PLabel(
            '', x=200, y=160, background=self.Background, foreground='red')

        self.add(self.lblErrorProc)

        self.btnAddProc = PButton('Agregar', x=290, y=190, cmd=self.add_proc)
        self.add(self.btnAddProc)

        self.add(PLabel(title='Quantum:', x=500,
                 y=50, background=self.Background))

        self.txtBoxQuantum = PTextBox(x=560, y=50, width=15)
        self.add(self.txtBoxQuantum)

        self.lblErrorQuantum = PLabel(
            '', x=500, y=70, background=self.Background, foreground='red')
        self.add(self.lblErrorQuantum)

        self.btnIniciar = PMenuCommand('Iniciar', cmd=self.start)

        self.MenuBar.add(self.btnIniciar)

        # Label para el DataGrid de los procesos
        self.add(PLabel(title='Procesos:', x=10,
                 y=215, background=self.Background))

        self.dataGrid = Treeview(self, columns=('#1', '#2', '#3'))

        self.dataGrid.column('#0', width=30, anchor=CENTER, minwidth=30)
        self.dataGrid.column('#1', width=80, anchor=CENTER, minwidth=65)
        self.dataGrid.column('#2', width=80, anchor=CENTER, minwidth=65)
        self.dataGrid.column('#3', width=80, anchor=CENTER, minwidth=65)

        self.dataGrid.heading('#0', text='Id')
        self.dataGrid.heading('#1', text='Nombre')
        self.dataGrid.heading('#2', text='Tiempo')
        self.dataGrid.heading('#3', text='E/S')

        self.dataGrid.insert('', END, text=1, values=('Proceso 1', 15, True))

        self.dataGrid.place(x=10, y=235)

        test = PDataGrid()
        test.add_column('Id', width=30, minwidth=30)
        test.add_column('Nombre', width=80, minwidth=65)
        test.add_column('Tiempo', width=80, minwidth=65)
        test.add_column('E/S', width=80, minwidth=65)

        for key in test.Columns:
            print(test.Columns[key])

    def add_proc(self):
        name = str(self.txtBoxNombreProc.Title).strip()
        time = str(self.txtBoxTiempoProc.Title).strip()

        if name == '' or time == '':
            self.lblErrorProc.Title = '* Nombre invalido o tiempo invalido.'
            return

        if not time.isdecimal():
            self.lblErrorProc.Title = '* Tiempo invalido [Tiene que ser un número].'
            return

        self.lblErrorProc.Title = ''
        print(f'{name=}')
        print(f'{int(time)=}')

        self.txtBoxTiempoProc.clear()
        self.txtBoxNombreProc.clear()

    def start(self):

        if self.btnIniciar.State != NORMAL:
            return

        quantum = str(self.txtBoxQuantum.Title)

        if not quantum.isdecimal():
            self.lblErrorQuantum.Title = '* Quantum invalido [Tiene que ser un número entero].'
            return

        self.lblErrorQuantum.Title = ''
        self.disable_widgets()

        print(f'{int(quantum)=}')

    def disable_widgets(self):
        self.btnIniciar.State = DISABLED
        self.txtBoxQuantum.State = DISABLED
        self.txtBoxNombreProc.State = DISABLED
        self.txtBoxTiempoProc.State = DISABLED
        self.btnAddProc.State = DISABLED


def main():
    f = RoundRobin()

    f.show()


if __name__ == '__main__':
    main()

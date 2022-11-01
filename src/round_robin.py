
import random
from time import sleep
from components.visual_models import *
from process import Process, READY, FINISHED, BLOCKED, RUNNING


class RoundRobin(PFrame):

    @property
    def ProcessList(self):
        return self._processList

    @property
    def ReadyProcesses(self):
        return self._readyProcesses

    @property
    def BlockedProcesses(self):
        return self._blockedProcesses

    @property
    def FinishedProcesses(self):
        return self._finishedProcesses

    @property
    def CurrentProcess(self):
        return self._currentProcess

    @CurrentProcess.setter
    def CurrentProcess(self, value: Process):
        self._currentProcess = value

    def __init__(self):
        super().__init__('Simulador', 800, 600)

        self._processList = list()
        self._readyProcesses = list()
        self._blockedProcesses = list()
        self._finishedProcesses = list()
        self._currentProcess = None
        self.index = 0

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

        self.cbEntradaSalida = PCheckBox(
            'Entrada/Salida', x=460, y=130, background=self.Background)
        self.add(self.cbEntradaSalida)

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

        self.dataGrid = PDataGrid(x=10, y=235)

        self.dataGrid.add_column('Id', width=30, minwidth=30)
        self.dataGrid.add_column('Nombre', width=80, minwidth=65)
        self.dataGrid.add_column('Tiempo', width=80, minwidth=65)
        self.dataGrid.add_column('E/S', width=80, minwidth=65)

        self.add(self.dataGrid)

    def add_proc(self):
        name = str(self.txtBoxNombreProc.Title).strip()
        time = str(self.txtBoxTiempoProc.Title).strip()
        isES = bool(self.cbEntradaSalida.Value)

        if name == '' or time == '':
            self.lblErrorProc.Title = '* Nombre invalido o tiempo invalido.'
            return

        if not time.isdecimal():
            self.lblErrorProc.Title = '* Tiempo invalido [Tiene que ser un número].'
            return

        self.index += 1

        process = Process(self.index, name, time, isES)

        if process.Name in [proc.Name for proc in self.ProcessList]:
            self.lblErrorProc.Title = '* Ese proceso ya está en la lista.'
            return

        self.ProcessList.append(process)

        self.dataGrid.add_row(process.toList())

        self.lblErrorProc.Title = ''
        self.txtBoxTiempoProc.clear()
        self.txtBoxNombreProc.clear()
        self.cbEntradaSalida.Value = False

    def start(self):

        if self.btnIniciar.State != NORMAL:
            return

        quantum = str(self.txtBoxQuantum.Title)

        if not quantum.isdecimal():
            self.lblErrorQuantum.Title = '* Quantum invalido [Tiene que ser un número entero].'
            return

        if len(self.ProcessList) == 0:
            self.lblErrorQuantum.Title = '* Debe de haber al menos un proceso.'
            return

        self.lblErrorQuantum.Title = ''
        self.lblErrorProc = ''
        self.disable_widgets()

        self.quantum = int(quantum)
        self._readyProcesses = self.ProcessList

        self.add(PPanel(x=290, y=245, width=100, height=26 +
                 25*len(self.ProcessList), borderwidth=3))
        self.add(PLabel('Listo', x=325, y=250))

        self.add(PPanel(x=400, y=245, width=100, height=26 +
                 25*1, borderwidth=3))
        self.add(PLabel('Corriendo', x=423, y=250))

        self.add(PPanel(x=510, y=245, width=100, height=26 +
                 25*len(self.ProcessList), borderwidth=3))
        self.add(PLabel('Terminado', x=530, y=250))

        self.add(PPanel(x=620, y=245, width=100, height=26 +
                 25*len(self.ProcessList), borderwidth=3))
        self.add(PLabel('Bloqueado', x=640, y=250))

        self.lblQuantum = PLabel(
            f'Quantum: {self.quantum}', x=450, y=215, background=self.Background)

        self.add(self.lblQuantum)

        self.lblsReady = list()
        self.lblsBlocked = list()
        self.lblsFinished = list()

        self.cargar_procesos()

        # Ejecutar el primero en la lista de listos
        self.update()
        sleep(1)

        initialSize = len(self.ProcessList)

        i = 0
        aux = -1
        while len(self.FinishedProcesses) != initialSize:

            # Revisar si hay procesos listos
            self.revisar_procesos_listos()
            if i == aux + 2: self.revisar_procesos_bloqueados()

            self.cargar_procesos(False)

            x = self.quantum - 1
            e_s = False
            triggerES = 0
            while x >= 0:

                if not isinstance(self.CurrentProcess, Process):
                    break

                # Proceso Entrada/Salida
                if self.CurrentProcess.IsInputOutput and not e_s:

                    triggerES = random.randint(
                        0, min(self.quantum, self.CurrentProcess.ActualQuantum))

                    print(f'{triggerES=}')

                    e_s = True
                if self.CurrentProcess.IsInputOutput: print(f'{min(x + 1, self.CurrentProcess.ActualQuantum)=}')
                # Interrupción E/S
                if e_s and min(x + 1, self.CurrentProcess.ActualQuantum) == triggerES and not self.CurrentProcess.HasBlocked:
                    self.CurrentProcess.State = BLOCKED

                    print(f'Bloqueando: {self.CurrentProcess.Name}')
                    aux = i

                    self.CurrentProcess.HasBlocked = True
                    self.BlockedProcesses.append(self.CurrentProcess)
                    self.CurrentProcess = None
                    self.lblRunning.destroy()
                    break

                self.lblQuantum.Title = f'Quantum: {x}'
                self.update()
                sleep(1)
                self.CurrentProcess.ActualQuantum -= 1

                # Termino el proceso
                if self.CurrentProcess.ActualQuantum == 0:
                    self.CurrentProcess.State = FINISHED

                    print(f'Finalizando: {self.CurrentProcess.Name}')

                    self.FinishedProcesses.append(self.CurrentProcess)
                    self.CurrentProcess = None
                    self.lblRunning.destroy()
                    break

                # Se acabo el tiempo
                if x == 0:
                    self.CurrentProcess.State = READY

                    print(f'Tiempo agotado: {self.CurrentProcess.Name}')

                    self.ReadyProcesses.append(self.CurrentProcess)
                    self.CurrentProcess = None
                    self.lblRunning.destroy()

                x -= 1

            self.cargar_procesos(False)
            i += 1

    def revisar_procesos_listos(self):
        if len(self.ReadyProcesses) == 0:
            return

        process = self.ReadyProcesses[0]

        if not isinstance(process, Process):
            return

        self.lblQuantum.Title = f'Quantum: {self.quantum}'

        self.ReadyProcesses.remove(process)
        process.State = RUNNING
        self.CurrentProcess = process

        print(f'Ejecutando: {self.CurrentProcess.Name}')

        self.lblRunning = PLabel(self.CurrentProcess.Name, x=410, y=270)
        self.add(self.lblRunning)

    def revisar_procesos_bloqueados(self):

        if len(self.BlockedProcesses) == 0:
            return

        process = self.BlockedProcesses[0]

        if not isinstance(process, Process):
            return

        self.BlockedProcesses.remove(process)
        print(f'Preparando: {process.Name}')
        process.State = READY
        self.ReadyProcesses.append(process)

    def cargar_procesos(self, once=True):
        self.cargar_procesos_listos(once)
        self.cargar_procesos_bloqueados(once)
        self.cargar_procesos_terminados(once)

    def cargar_procesos_listos(self, once=True):

        for lbl in self.lblsReady:

            if not isinstance(lbl, PLabel):
                continue

            lbl.destroy()

        i = 1
        self.lblsReady = list()

        for p in self.ReadyProcesses:
            self.lblsReady.append(PLabel(p.Name, x=300, y=250 + 20*i))
            i += 1

        # Cargar los procesos
        for lbl in self.lblsReady:
            self.update()
            if once:
                sleep(0.5)
            self.add(lbl)

    def cargar_procesos_bloqueados(self, once=True):

        for lbl in self.lblsBlocked:

            if not isinstance(lbl, PLabel):
                continue

            lbl.destroy()

        i = 1
        self.lblsBlocked = list()

        for p in self.BlockedProcesses:
            self.lblsBlocked.append(PLabel(p.Name, x=630, y=250 + 20*i))
            i += 1

        # Cargar los procesos
        for lbl in self.lblsBlocked:
            self.update()
            if once:
                sleep(0.5)
            self.add(lbl)

    def cargar_procesos_terminados(self, once=True):
        for lbl in self.lblsFinished:

            if not isinstance(lbl, PLabel):
                continue

            lbl.destroy()

        i = 1
        self.lblsFinished = list()

        for p in self.FinishedProcesses:
            self.lblsFinished.append(PLabel(p.Name, x=520, y=250 + 20*i))
            i += 1

        # Cargar los procesos
        for lbl in self.lblsFinished:
            self.update()
            if once:
                sleep(0.5)
            self.add(lbl)

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

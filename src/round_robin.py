
from decimal import ROUND_HALF_UP, Decimal
import random
from time import sleep
from components.visual_models import *
from process import Process, READY, FINISHED, BLOCKED, RUNNING


def round_well(num: float):
    return int(Decimal(num).quantize(0, ROUND_HALF_UP))


def round_str(str: str):
    return round_well(len(str)/2)


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
        super().__init__('Simulador', 1000, 600)

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

        posX = 20
        posY = 20

        # Label para la aprte de agregar procesos
        self.add(PLabel(title='Agregar procesos:', x=posX,
                 y=posY, background=self.Background))

        lblNomY = posY + 50
        lblNomX = posX
        # Label para el TextBox nombre del proceso
        self.add(PLabel(title='Nombre:', x=lblNomX,
                 y=lblNomY, background=self.Background))

        txtNomX = lblNomX
        txtNomY = lblNomY + 30
        self.txtBoxNombreProc = PTextBox(x=txtNomX, y=txtNomY, width=15)
        self.add(self.txtBoxNombreProc)

        # Label para el TextBox tiempo del proceso
        lblTimeX = lblNomX + 200
        lblTimeY = lblNomY
        self.add(PLabel(title='Tiempo:', x=lblTimeX,
                 y=lblTimeY, background=self.Background))

        txtTimeX = lblTimeX
        txtTimeY = lblTimeY + 30
        self.txtBoxTiempoProc = PTextBox(x=txtTimeX, y=txtTimeY, width=15)
        self.add(self.txtBoxTiempoProc)

        cbPosX = txtTimeX + 200
        cbPosY = txtTimeY
        self.cbEntradaSalida = PCheckBox(
            'Entrada/Salida', x=cbPosX, y=cbPosY, background=self.Background)
        self.add(self.cbEntradaSalida)

        lblErrorX = lblNomX
        lblErrorY = txtNomY + 35
        self.lblErrorProc = PLabel(
            '', x=lblErrorX, y=lblErrorY, background=self.Background, foreground='red')

        self.add(self.lblErrorProc)

        btnAddX = txtTimeX - 70
        btnAddY = lblErrorY + 30
        self.btnAddProc = PButton(
            'Agregar', x=btnAddX, y=btnAddY, cmd=self.add_proc)
        self.add(self.btnAddProc)

        self.lblQuantumX = cbPosX
        self.lblQuantumY = posY
        self.add(PLabel(title='Quantum:', x=self.lblQuantumX,
                 y=self.lblQuantumY, background=self.Background))

        txtQuantumX = self.lblQuantumX + 90
        txtQuantumY = self.lblQuantumY
        self.txtBoxQuantum = PTextBox(x=txtQuantumX, y=txtQuantumY, width=15)
        self.add(self.txtBoxQuantum)

        lblErrorQuantumX = self.lblQuantumX
        lblErrorQuantumY = txtQuantumY + 40
        self.lblErrorQuantum = PLabel(
            '', x=lblErrorQuantumX, y=lblErrorQuantumY, background=self.Background, foreground='red')
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

        self.pnlReadyX = 290
        self.pnlReadyY = 245
        width = 150
        height = 35
        count_listprocess = len(self.ProcessList)

        self.add(PPanel(x=self.pnlReadyX, y=self.pnlReadyY, width=width, height=height +
                 25*count_listprocess, borderwidth=3))
        self.add(PLabel('Listo', x=self.pnlReadyX + width //
                 round_str('Listo'), y=self.pnlReadyY + 10))

        self.pnlRunningX = self.pnlReadyX + width + 10
        self.pnlRunningY = self.pnlReadyY
        self.add(PPanel(x=self.pnlRunningX, y=self.pnlRunningY, width=width, height=height +
                 25*1, borderwidth=3))
        self.add(PLabel('Corriendo', x=self.pnlRunningX + width //
                 round_str('Corriendo'), y=self.pnlRunningY + 10))

        self.pnlFinishedX = self.pnlRunningX + width + 10
        self.pnlFinishedY = self.pnlRunningY
        self.add(PPanel(x=self.pnlFinishedX, y=self.pnlFinishedY, width=width, height=height +
                 25*count_listprocess, borderwidth=3))
        self.add(PLabel('Terminado', x=self.pnlFinishedX + width //
                 round_str('Terminado'), y=self.pnlFinishedY + 10))

        self.pnlBlockedX = self.pnlFinishedX + width + 10
        self.pnlBlockedY = self.pnlFinishedY
        self.add(PPanel(x=self.pnlBlockedX, y=self.pnlBlockedY, width=width, height=height +
                 25*count_listprocess, borderwidth=3))
        self.add(PLabel('Bloqueado', x=self.pnlBlockedX + width //
                 round_str('Bloqueado'), y=self.pnlBlockedY + 10))

        self.lblQuantumX = self.pnlRunningX + 100
        self.lblQuantumY = self.pnlRunningY - 30
        self.lblQuantum = PLabel(
            f'Quantum: {self.quantum}', x=self.lblQuantumX, y=self.lblQuantumY, background=self.Background)

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
            if i == aux + 2:
                self.revisar_procesos_bloqueados()

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

                    e_s = True
                    
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

        self.lblRunning = PLabel(self.CurrentProcess.Name, x=self.pnlRunningX + 10, y=self.pnlRunningY + 30)
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
            self.lblsReady.append(PLabel(p.Name, x=self.pnlReadyX + 10, y=self.pnlReadyY + 10 + 20*i))
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
            self.lblsBlocked.append(PLabel(p.Name, x=self.pnlBlockedX + 10, y=self.pnlBlockedX + 10 + 20*i))
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
            self.lblsFinished.append(PLabel(p.Name, x=self.pnlFinishedX + 10, y=self.pnlFinishedY + 10 + 20*i))
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

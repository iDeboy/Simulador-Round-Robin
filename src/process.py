
from typing import Literal


READY = 'ready'
RUNNING = 'running'
BLOCKED = 'blocked'
FINISHED = 'finished'

class Process:

    @property
    def Id(self):
        return self._id

    @Id.setter
    def Id(self, value: int):
        self._id = int(value)

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, value: str):
        self._name = str(value)

    @property
    def Quantum(self):
        return self._quantum

    @Quantum.setter
    def Quantum(self, value: int):
        self._quantum = int(value)

    @property
    def IsInputOutput(self):
        return self._isInputOutput

    @IsInputOutput.setter
    def IsInputOutput(self, value: bool):
        self._isInputOutput = bool(value)

    @property
    def State(self):
        return self._state

    @State.setter
    def State(self, value: Literal['ready', 'running', 'blocked', 'finished']):
        self._state = str(value)

    @property
    def ActualQuantum(self):
        return self._actualQuantum

    @ActualQuantum.setter
    def ActualQuantum(self, value: int):
        self._actualQuantum = int(value)

    @property
    def HasBlocked(self):
        return self._hasblocked
    
    @HasBlocked.setter
    def HasBlocked(self, value: bool):
        self._hasblocked = bool(value)

    def __init__(self, id = 0, name = 'Process', quantum = 0, isInputOutput = False, state = READY):
        
        self.Id = id
        self.Name = name
        self.Quantum = quantum
        self.IsInputOutput = isInputOutput
        self.State = state
        self.ActualQuantum = self.Quantum
        self.HasBlocked = False

    def toList(self):
        values = list()
        values.append(self.Id)
        values.append(self.Name)
        values.append(self.Quantum)
        values.append(self.IsInputOutput)

        return values

    
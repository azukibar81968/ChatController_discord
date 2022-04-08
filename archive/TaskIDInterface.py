from abc import ABC, abstractmethod

class TaskIDInterface(ABC):
    @abstractmethod
    def GetTaskID(self):
        pass
from abc import ABC, abstractmethod

class ScoreingInterface(ABC):
    @abstractmethod
    def Scoreing(self, message):
        return 0

    
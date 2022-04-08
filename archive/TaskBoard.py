class TaskBoard:
    def __init__(self):
        self._TaskBoard = []  # List of ScoreingInterface

    def GetTask(self, i):
        return self._TaskBoard[i]

    def GetTaskList(self):
        return self._TaskBoard

    def AddTail(self, task):
        self._TaskBoard.append(task)

    def AddHead(self, task):
        self._TaskBoard.insert(0,task)

    def GetHead(self):
        return self._TaskBoard[0]

    def GetTail(self):
        return self._TaskBoard[len(self._TaskBoard)-1]

    def GetLen(self):
        return len(self._TaskBoard)
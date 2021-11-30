import TaskIDInterface
import TaskBoard

class GenerateDialig:

    def __init__(self):
        self._taskBoard = TaskBoard.TaskBoard()

    def addTask(self, task):
        self._taskBoard.AddHead(task)

    def GetReplyList(self):
        reply = ""
        print(self._taskBoard.GetHead().GetTaskID())
        if self._taskBoard.GetHead().GetTaskID() == "turnOnAC":
            reply = ["はーい"]
        else:
            reply = ["はいはい"]

        return reply
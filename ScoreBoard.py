import ScoreingInterface
import TaskBoard

class ScoreBoard:

    def __init__(self, taskBoard):
        self.taskBoard = taskBoard

    def CalcScore(self, message):
        taskBuf = {}
        for t in self.taskBoard.GetTaskList():
            score = t.Scoreing(message)
            taskBuf[t] = score
        
        return taskBuf

    def ChoiseTask(self, message):
        taskBuf = self.CalcScore(message)
        maxScore = max(taskBuf.values())
        tasks = [k for k, v in taskBuf.items() if v == maxScore]

        return tasks[0]
import ScoreBoard
import DealTaskInterface
import GenerateDialog

class Dealer:
    def __init__(self,board):
        self._board = board
        self._DialogGenerator = GenerateDialog.GenerateDialig()
        

    def dealMessage(self, message):
        task = self._board.ChoiseTask(message)
        task.DealTask()
        self._DialogGenerator.addTask(task)
        replyList = self._DialogGenerator.GetReplyList()
        return replyList
    


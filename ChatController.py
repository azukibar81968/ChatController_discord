import ConcreteTask
import Dealer
import DealTaskInterface
import MessageParser
import ScoreBoard
import ScoreingInterface
import TaskBoard

class ChatController:
    def __init__(self):
        self._turnOnAircon = ConcreteTask.turnOnAirConditioner("turnOnAC")
        self._turnOffAircon = ConcreteTask.turnOffAirConditioner("turnOffAC")
        self._turnOnLight = ConcreteTask.turnOnLight("turnOnLight")
        self._turnOffLight = ConcreteTask.turnOffLight("turnOffLight")

        self._board = TaskBoard.TaskBoard()
        self._board.AddTail(self._turnOnAircon)
        self._board.AddTail(self._turnOffAircon)
        self._board.AddTail(self._turnOnLight)
        self._board.AddTail(self._turnOffLight)

        self._scoreBoard = ScoreBoard.ScoreBoard(self._board)

        self._dealer = Dealer.Dealer(self._scoreBoard)

    def dealMessage(self, message):
        return self._dealer.dealMessage(message)



if __name__ == "__main__":
    ctrl = ChatController()
    while True:
        i = input()
        replyList = ctrl.dealMessage(i)
        for rep in replyList:
            print(rep)

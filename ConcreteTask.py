import ScoreingInterface
import DealTaskInterface
import TaskIDInterface
import MessageParser
from abc import ABC

SCORE_GLOBAL = 1

class ContainerList:
    def __init__(self, *containers):
        self._ContainerList = containers
        self._BestContainerIndex = -1

    def setIndex(self, ind):
        self._BestContainerIndex = ind

    def getBestContainer(self):
        return self._ContainerList[self._BestContainerIndex]

    def getContainers(self):
        return self._ContainerList

class Container:
    def __init__(self, message):
        self.message = message
        self._optionList = {} #need to add task

    def compile(self): #need to override
        # <task>(<option>:<container>,<option>:<container>) の文字列を返すようにする
        return ""

    def _calcSelfScore(self): #need to override
        #messageに対する自身のスコアを返す
        return 0

    def _evalBestContainer(self):

        for option, containerList in self._optionList.items():
            maxScore = -1
            cur = -1
            cnt = 0

            for container in containerList.getContainers():
                if maxScore < container.calcScore():
                    maxScore = container.calcScore()
                    cur = cnt

                cnt += 1

            self._optionList[option].setIndex(cur)
            

    def calcScore(self):
        score = 0
        for _, containerList in self._optionList.items(): #自分のContainerのスコアを全て計算
            optionScore = containerList.getBestContainer().calcScore()
            score += optionScore

        score += self._calcSelfScore() #自分のスコアを加算
        return score



class airConditionerCard(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {
            "action": ContainerList(
                airconditionerActionOff(message),
                airconditionerActionOn(message),
            )
        }
        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        if mp.IsContainTurget("エアコン") or mp.IsContainTurget("冷房") or mp.IsContainTurget("暖房") or mp.IsContainTurget("除湿"):
            score += 1
                
        return score

    def compile(self):
        res = "airconditioner ( action :" + self._optionList["action"].getBestContainer().compile() + ")"
        return res


class airconditionerActionOn(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {
            "temp": ContainerList(
                airconditionerTemp(message)
            ),
            "time": ContainerList(
                airconditionerTimeAM(message),
                airconditionerTimePM(message)
            ),
            "mode": ContainerList(
                airconditionerModeHot(message),
                airconditionerModeCool(message),
                airconditionerModeHumid(message)
            )
        }
        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0
        turgetVerbList = mp.GetTurgetVerb("エアコン")
        
        if "つけ" in turgetVerbList or "焚い" in turgetVerbList:
            #TODO: 焚く、焚い、焚きあたりを全部検出したい。MessageParserの改良が必要
            score = 1

        return score
        


    def compile(self):
        timeCom = self._optionList["time"].getBestContainer().compile()
        tempCom = self._optionList["temp"].getBestContainer().compile()
        modeCom = self._optionList["mode"].getBestContainer().compile()
        res = "on ( time : " + timeCom + ", temp : " + tempCom + ", mode : " + modeCom + ")"
        return res


class airconditionerActionOff(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {
            "time": ContainerList(
                airconditionerTimeAM(message),
                airconditionerTimePM(message)
            )
        }
        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        turgetVerbList =  mp.GetTurgetVerb("エアコン")
        if "消し" in turgetVerbList or "けし" in turgetVerbList:
            #TODO: 焚く、焚い、焚きあたりを全部検出したい。MessageParserの改良が必要
            score = 1

        return score
        


    def compile(self):
        timeCom = self._optionList["time"].getBestContainer().compile()
        res = "off ( time : " + timeCom + ")"
        return res




class airconditionerModeCool(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        if mp.IsContainTurget("冷房"):
            score = 1
        return score

    def compile(self):
        return "cool"


class airconditionerModeHot(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}

    def calcScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        if mp.IsContainTurget("暖房"):
            score = 1

        return score

    def compile(self):
        return "hot"



class airconditionerModeHumid(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._evalBestContainer()

    def calcScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        if mp.IsContainTurget("除湿"):
            score = 1

        return score

    def compile(self):
        return "hot"


class airconditionerTimeAM(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._evalBestContainer()

    def calcScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0
        if mp.IsContainTurget("午前"):
            score = 1

        #print("AM score = " + str(score))
        return score

    def compile(self):
        return "AM"

class airconditionerTimePM(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._evalBestContainer()

    def calcScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        if mp.IsContainTurget("午後"):
            score = 1
        #print("PM score = " + str(score))
        return score

    def compile(self):
        return "PM"


class airconditionerTemp(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._evalBestContainer()

    def calcScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        if mp.IsContainTurget("度"):
            score = 1

        return score

    def compile(self):
        return "28"






if __name__ == "__main__":
    print("----------")

    text01 = "午後になったらエアコンを消しておいてちょうだい"
    print(text01)
    container = airConditionerCard(text01)
    print(container.compile())

    print("----------")

    text02 = "午前になったら28度の暖房でエアコンをつけておいてくれるかな？"
    print(text02)
    container = airConditionerCard(text02)
    print(container.compile())

    print("----------")

    text02 = "午前になったら28度の冷房でエアコンをつけておいてくれる？"
    print(text02)
    container = airConditionerCard(text02)
    print(container.compile())








#################################################

def isContainNouns(message, wordlist):
    p = MessageParser.MessageParser(message)
    ans = 0
    for w in wordlist:
        if w in p.GetNouns():
            ans = SCORE_GLOBAL
    return ans


def isContainVerb(message, wordlist):
    p = MessageParser.MessageParser(message)
    ans = 0
    for w in wordlist:
        if w in p.GetVerb()[0]:
            ans = SCORE_GLOBAL
    return ans


def isContainAirConditioner(message):
    airConditionerWord = ["エアコン", "冷房", "暖房", "空調"]

    return isContainNouns(message, airConditionerWord)


def isContainLight(message):
    lightsWord = ["電気", "電灯", "あかり", "灯"]

    return isContainNouns(message, lightsWord)



class turnOnAirConditioner(ScoreingInterface.ScoreingInterface, DealTaskInterface.DealTaskInterface, TaskIDInterface.TaskIDInterface):
    def __init__(self, taskID):
        self.taskID=taskID

    def GetTaskID(self):
        return self.taskID

    def isContainTurnOn(self, message):
        turnOnWord=["つけ", "焚", "炊"]
        return isContainVerb(message, turnOnWord)

    def Scoreing(self, message):
        return isContainAirConditioner(message) + self.isContainTurnOn(message)

    def DealTask(self):
        print("task deal...   Turn on the airConditioner")


class turnOffAirConditioner(ScoreingInterface.ScoreingInterface, DealTaskInterface.DealTaskInterface, TaskIDInterface.TaskIDInterface):
    def __init__(self, taskID):
        self.taskID=taskID

    def GetTaskID(self):
        return self.taskID

    def isContainTurnOff(self, message):
        turnOffWord=["消"]
        return isContainVerb(message, turnOffWord)

    def Scoreing(self, message):
        return isContainAirConditioner(message) + self.isContainTurnOff(message)

    def DealTask(self):
        print("task deal...   Turn off the airConditioner")


class turnOnLight(ScoreingInterface.ScoreingInterface, DealTaskInterface.DealTaskInterface, TaskIDInterface.TaskIDInterface):
    turnOnWord=["つけ"]
    def __init__(self, taskID):
        self.taskID=taskID

    def GetTaskID(self):
        return self.taskID

    def isContainTurnOn(self, message):
        turnOnWord=["つけ"]
        return isContainVerb(message, turnOnWord)

    def Scoreing(self, message):
        return isContainLight(message) + self.isContainTurnOn(message)

    def DealTask(self):
        print("task deal...   Turn on the light")


class turnOffLight(ScoreingInterface.ScoreingInterface, DealTaskInterface.DealTaskInterface):
    turnOffWord=["消"]
    def __init__(self, taskID):
        self.taskID=taskID

    def GetTaskID(self):
        return self.taskID

    def isContainTurnOff(self, message):
        turnOffWord=["消"]
        return isContainVerb(message, turnOffWord)

    def Scoreing(self, message):
        return isContainLight(message) + self.isContainTurnOff(message)

    def DealTask(self):
        print("task deal...   Turn off the light")

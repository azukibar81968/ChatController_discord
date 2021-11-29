import ScoreingInterface
import DealTaskInterface
import TaskIDInterface
import MessageParser
from abc import ABC
import json

SCORE_GLOBAL = 1
SCORE_EQUAL = 0
############

"""""""""""
###structure of container###

container = {
    'head' : '<containerName>',
    'option' : 
    {
        <option1> : container,
        <option2> : container,
        ...
        ...
    }
}

ex:

午前になったら28度の冷房でエアコンをつけておいてくれる？

={
	"head": "loot",
	"option": {
		"task": {
			"head": "airconditioner",
			"option": {
				"action": {
					"head": "on",
					"option": {
						"?temp": "28",
						"?time": "AM",
						"mode": "cool"
					}
				}
			}
		}
	}
}

loot 
  L task : airconditioner
      L action : turnOn
          L temp : 28度
              L mode : Cool
              L time : TimeNum
                  L hour : 22
                  L minute : 30

"""""""""""

############

class ContainerList:
    def __init__(self, *containers):
        self._ContainerList = containers
        self._BestContainerIndex = -1
        self._unidentifiableFlg = False

    def setIndex(self, ind):
        self._BestContainerIndex = ind

    def getBestContainer(self):
        if self._BestContainerIndex >= 0:
            return self._ContainerList[self._BestContainerIndex]
        else:
            return VoidContainer("")

    def getContainers(self):
        return self._ContainerList

class Container:
    def __init__(self, message):
        self.message = message
        self._optionList = {} #need to add task
        self._ContainerName = "" #need to edit to ContainerName (ex: temp)

    def compile(self): #DON'T override
        #<task>(<option>:<container>,<option>:<container>)の文字列を返すようにする

        optionDict = {}
        for optionName, optionContainerList in self._optionList.items():
            optionContainer = optionContainerList.getBestContainer()
            if optionContainer._ContainerName == "UNIDENTIFIABLE":
                if optionName[0] == "?":
                    continue

            optionDict[optionName] = optionContainer.compile()


        compileDict = {
            "head" : self._ContainerName,
            "option" : optionDict
        }
 
        return compileDict

    def _evalBestContainer(self):#DON'T override

        for option, containerList in self._optionList.items():
            maxScore = -1
            minDiff = 9999999999999999999999999999999
            cur = -1
            cnt = 0


            for container in containerList.getContainers():
                containerScore =  container.calcScore()
                if maxScore < containerScore:
                    maxScore = containerScore
                    cur = cnt

                cnt += 1

            for container in containerList.getContainers():
                containerScore = container.calcScore()
                if minDiff > abs(maxScore - containerScore) and 0 < abs(maxScore - containerScore):
                    minDiff = abs(maxScore - containerScore)


            #print("option :: " + option + "---mindif = " + str(minDiff))
            if minDiff < SCORE_EQUAL:
                #print("score equal!!!!!")
                cur = -1
            if maxScore == 0:
                #print("score zero!!!!!")
                cur = -1


            self._optionList[option].setIndex(cur)
            

    def calcScore(self):#DON'T override
        score = 0
        for _, containerList in self._optionList.items(): #自分のContainerのスコアを全て計算
            optionScore = containerList.getBestContainer().calcScore()
            score += optionScore

        score += self._calcSelfScore() #自分のスコアを加算
        #print("container name = " + self._ContainerName + "::: score = " + str(score))
        return score

    def _calcSelfScore(self): #need to override
        #messageに対する自身のスコアを返す
        return 0



class VoidContainer(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._ContainerName = "UNIDENTIFIABLE"

        self._evalBestContainer()

    def _calcSelfScore(self):
        return 0

    def compile(self):
        return "UNIDENTIFIABLE"


class lootConditioner(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {
            "task": ContainerList(
                airConditioner(message),
                light(message),
            )
        }
        self._ContainerName = "loot"

        self._evalBestContainer()



######air conditioner######
class airConditioner(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {
            "action": ContainerList(
                airconditionerActionOff(message),
                airconditionerActionOn(message),
            )
        }
        self._ContainerName = "airconditioner"

        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        if mp.IsContainTurget("エアコン") or mp.IsContainTurget("冷房") or mp.IsContainTurget("暖房") or mp.IsContainTurget("除湿"):
            score += 1
                
        return score



class airconditionerActionOn(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {
            "?temp": ContainerList(
                airconditionerTemp(message)
            ),
            "?time": ContainerList(
                timeAM(message),
                timePM(message),
                timeNum(message)
            ),
            "mode": ContainerList(
                airconditionerModeHot(message),
                airconditionerModeCool(message),
                airconditionerModeHumid(message)
            )
        }
        self._ContainerName = "on"

        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0
        turgetVerbList = mp.GetTurgetVerb("エアコン")
        
        if "つけ" in turgetVerbList or "焚い" in turgetVerbList:
            #TODO: 焚く、焚い、焚きあたりを全部検出したい。MessageParserの改良が必要
            score = 1

        return score
        
class airconditionerActionOff(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {
            "?time": ContainerList(
                timeAM(message),
                timePM(message),
                timeNum(message)
            )
        }
        self._ContainerName = "off"
        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        turgetVerbList =  mp.GetTurgetVerb("エアコン")
        if "消し" in turgetVerbList or "けし" in turgetVerbList:
            #TODO: 焚く、焚い、焚きあたりを全部検出したい。MessageParserの改良が必要
            score = 1

        return score


class airconditionerModeCool(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._ContainerName = "cool"
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
        self._ContainerName = "hot"

    def _calcSelfScore(self):
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
        self._ContainerName = "humid"
        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        if mp.IsContainTurget("除湿"):
            score = 1

        return score

    def compile(self):
        return "humid"


class timeAM(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._ContainerName = "AM"
        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0
        if mp.IsContainTurget("午前"):
            score = 1

        #print("AM score = " + str(score))
        return score

    def compile(self):
        return "AM"

class timePM(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._ContainerName = "PM"
        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        if mp.IsContainTurget("午後"):
            score = 1
        #print("PM score = " + str(score))
        return score

    def compile(self):
        return "PM"

class timeNum(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {
            "hour": ContainerList(
                timeNumHour(message)
            ),
            "?minute": ContainerList(
                timeNumMinute(message)
            )
        }
        self._ContainerName = "TimeNum"
        self._evalBestContainer()


    def _calcSelfScore(self):
        score = 0
        return score


class timeNumHour(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._evalBestContainer()
        self._hour = -1

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        numDataList = mp.GetNumDataList()

        score = 0
        for i in numDataList:
            if i[1] == "時" and 0 <= i[0] and i[0] <= 24:
                score = 1
                self._hour = i[0]
        return score

    def compile(self):
        return str(self._hour)


class timeNumMinute(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._evalBestContainer()
        self._minute = -1

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        numDataList = mp.GetNumDataList()

        score = 0
        for i in numDataList:
            if i[1] == "分" and 0 <= i[0] and i[0] <= 60:
                score = 1
                self._minute = i[0]

        return score

    def compile(self):
        return str(self._minute)

class airconditionerTemp(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._evalBestContainer()
        self._temp = -1

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        numDataList = mp.GetNumDataList()

        score = 0
        for i in numDataList:
            if i[1] == "度":
                score = 1
                self._temp = i[0]


        return score

    def compile(self):
        return str(self._temp)


##### Light #####
class light(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {
            "action": ContainerList(
                lightActionOff(message),
                lightActionOn(message),
            )
        }
        self._ContainerName = "light"

        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        if mp.IsContainTurget("電灯") or mp.IsContainTurget("電気") or mp.IsContainTurget("あかり") or mp.IsContainTurget("灯"):
            score += 1
                
        return score



class lightActionOn(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {
            "?time": ContainerList(
                timeAM(message),
                timePM(message),
                timeNum(message)
            ),
            "?mode": ContainerList(
                lightModeNight(message)            )
        }
        self._ContainerName = "on"

        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0
        turgetVerbList = mp.GetTurgetVerb("電気")
        turgetVerbList += mp.GetTurgetVerb("灯")
        turgetVerbList += mp.GetTurgetVerb("あかり")
        
        if "つけ" in turgetVerbList:
            score = 1

        return score
        
class lightActionOff(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {
            "?time": ContainerList(
                timeAM(message),
                timePM(message),
                timeNum(message)
            )
        }
        self._ContainerName = "off"
        self._evalBestContainer()

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        turgetVerbList = mp.GetTurgetVerb("電気")
        turgetVerbList += mp.GetTurgetVerb("灯")
        turgetVerbList += mp.GetTurgetVerb("あかり")
        if "消し" in turgetVerbList or "けし" in turgetVerbList:
            score = 1

        return score


class lightModeNight(Container):
    def __init__(self, message):
        super().__init__(message)
        self._optionList = {}
        self._ContainerName = "night"
        self._evalBestContainer()
        

    def _calcSelfScore(self):
        mp = MessageParser.MessageParser(self.message)
        score = 0

        if mp.IsContainTurget("常夜灯") or mp.IsContainTurget("豆電"):
            score = 1
        return score

    def compile(self):
        return "night"




if __name__ == "__main__":
    print("----------")

    text01 = "午後になったらエアコンを消しておいてちょうだい"
    print(text01)
    container = lootConditioner(text01)
    print(container.compile())

    print("----------")

    text02 = "ね、22時30分になったら21度の暖房でエアコンをつけておいてくれるかな？"
    print(text02)
    container = lootConditioner(text02)
    print(container.compile())

    print("----------")

    text02 = "午前になったら28度の冷房でエアコンをつけておいてくれる？"
    print(text02)
    container = lootConditioner(text02)
    print(container.compile())

    print("----------")

    text02 = "エアコンをつけて"
    print(text02)
    container = lootConditioner(text02)
    print(container.compile())

    print("----------")

    text02 = "電気をつけて"
    print(text02)
    container = lootConditioner(text02)
    print(container.compile())

    print("----------")

    text02 = "灯りを常夜灯でつけて"
    print(text02)
    container = lootConditioner(text02)
    print(container.compile())



    print("----------")

    text02 = "電気を10時になったらつけて"
    print(text02)
    container = lootConditioner(text02)
    print(container.compile())

    print("----------")

    text02 = "エアコン暖房つけてよ"
    print(text02)
    container = lootConditioner(text02)
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



{"head": "airconditioner", "opttion": [{"action": "{\"head\": \"on\", \"opttion\": [{\"temp\": \"21\"}, {\"time\": \"{ hour :22 , minute : 30 }\"}, {\"mode\": \"hot\"}]}"}]}
import ScoreingInterface
import DealTaskInterface
import TaskIDInterface
import MessageParser
from abc import ABC

SCORE_GLOBAL = 1


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

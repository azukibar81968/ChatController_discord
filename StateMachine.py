import sys
from statistics import mode
from transitions.extensions import GraphMachine
from transitions import State
import xml.etree.ElementTree as ET
import pprint
import time
import random
import sqlInterface
import discordConnector

class stateMachine(object):

    def __init__(self, source) -> None:
        # XMLをもとに構造をつくる
        # 適切な配列に格納
        self.headName = "Initial"
        self.finalName = "Final"

        tree = ET.parse(source)
        root = tree.getroot()
        statesList = []
        transitionsList = []

        for s in root:            
        #  states
            if s.tag == "{http://www.w3.org/2005/07/scxml}state":
                for invoke in s:
                    botname = ""
                    if invoke.tag == "{http://www.w3.org/2005/07/scxml}invoke":
                        botname = invoke.attrib["src"]
                    statesList.append(State(name=s.attrib["id"], on_exit=["action_on_exit_"+botname]))
        #  transitions
                for t in s:
                    if t.tag == "{http://www.w3.org/2005/07/scxml}transition":
                        transition = {
                            "trigger" : t.attrib["event"],
                            "source" : s.attrib["id"],
                            "dest" : t.attrib["target"],
                            "prepare" : None
                        }
                        transitionsList.append(transition)

        # pprint.pprint(statesList)
        # pprint.pprint(transitionsList)

        self.statesMachine = callbackStates()
        self.machine = GraphMachine(model = self.statesMachine, states = statesList, transitions = transitionsList, initial = self.headName, auto_transitions=False)



    def run(self):
        while True:
            nowName = self.statesMachine.state       # 自分の状態をみる
            if nowName == self.finalName: # 終端なら終了
                break

            triggerList = self.machine.get_triggers(nowName)# 遷移先を一覧で取得
            choise = random.choice(triggerList)# ランダムに遷移先を決定
            self.statesMachine.trigger(choise)# 状態を更新
            

            time.sleep(2*random.random())

        print("talk sequence finish!!")


class callbackStates:#コールバック設定用のインナークラス
    def __init__(self) -> None:
        self.sqlIF = sqlInterface.SQLInterface()
        self.dc = discordConnector.discordConnector()

    def let_speak(self, speaker):#状態遷移前に呼ばれます！！
        nowName = self.state
        # 状態を元に、DBにアクセスして対話内容をひっぱってくる
        reply = self.sqlIF.select(["body"], ["aatalk"], ["symbol", "'"+nowName+"'", "="])[0][0]

        # asyncModuleのSendMessageで送る
        print("sending a-atalk: reply *{}*".format(reply))
        self.dc.makeReply(reply, speaker)
        pass

    def action_on_exit_bot1(self):
        self.let_speak("bot1")

    def action_on_exit_bot2(self):
        self.let_speak("bot2")

if __name__ == "__main__":
    
    m = stateMachine("weather_temp_hi.xml")

    filename = 'model.png'
    m.machine.get_graph().draw(filename, prog='dot', format='png')

    m.run()
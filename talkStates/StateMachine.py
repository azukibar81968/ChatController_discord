import sys
sys.path.append('..')
from statistics import mode
from transitions.extensions import GraphMachine
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
        self.sqlIF = sqlInterface.SQLInterface()
        self.dc = discordConnector.discordConnector()

        tree = ET.parse(source)
        root = tree.getroot()
        statesList = []
        transitionsList = []

        for s in root:            
        #  states
            if s.tag == "{http://www.w3.org/2005/07/scxml}state":
                statesList.append(s.attrib["id"])
        #  transitions
                for t in s:
                    if t.tag == "{http://www.w3.org/2005/07/scxml}transition":
                        transition = {
                            "trigger" : t.attrib["event"],
                            "source" : s.attrib["id"],
                            "dest" : t.attrib["target"],
                            "prepare" : "stateAction"
                        }
                        transitionsList.append(transition)

        # pprint.pprint(statesList)
        # pprint.pprint(transitionsList)

        self.statesMachine = callbackStates()
        self.machine = GraphMachine(model = self.statesMachine, states = statesList, transitions = transitionsList, initial = self.headName, auto_transitions=False)



    def run(self):
        while True:
            # 自分の状態をみる
            nowName = self.statesMachine.state
            if nowName == self.finalName:
                break

            # 状態を元に、DBにアクセスして対話内容をひっぱってくる
            reply = self.sqlIF.select(["body"], ["aatalk"], ["symbol", "'"+nowName+"'", "="])[0]

            # asyncModuleのSendMessageで送る
            print("sending a-atalk: reply *{}*".format(reply))
            self.dc.makeReply(reply, "bot2")#TODO: 複数Botを交互に選択するようにしたい。情報はXMLのinvokeに入っている

            # 状態を更新
            # 選択肢を一覧で取得
            triggerList = self.machine.get_triggers(nowName)
            choise = random.choice(triggerList)
            self.statesMachine.trigger(choise)

            time.sleep(2*random.random())

        print("talk sequence finish!!")


class callbackStates:#コールバック設定用のインナークラス
    def stateAction(self):#状態遷移前に呼ばれます！！
        pass


if __name__ == "__main__":
    
    m = stateMachine("weather_temp_hi.xml")

    filename = 'model.png'
    m.machine.get_graph().draw(filename, prog='dot', format='png')

    m.run()
import ConcreteTask
import MessageParser
import singleton
import MessageParser
import json
import urllib
import switchbotConnenctor

"""""

dealMessageを設計する

dealMessage:
  input :  (str) Discordから来たメッセージ一件
  output:  (list<str>) Discordに送信するメッセージ
  備考   :  入力に応じて家電を動かす必要があれば動かす

Memo:
outputは
[
    {<botName1> : <replyMessage1>}
    {<botName2> : <replyMessage2>}
    {<botName3> : <replyMessage3>}
    ...
]
にアップデート予定
"""""


class ChatController:
    def __init__(self):
        self._dealer = ChatSequence()

    def dealMessage(self, message):
        return self._dealer.dealMessage(message)



class ChatSequence(singleton.Singleton):
    def __init__(self):
        self.chatSequence = []
    
    def dealMessage(self,message):
        if len(self.chatSequence) == 0:
            self._startChatSequence(message)

        while 1:
            if len(self.chatSequence) == 0:
                break
            self.chatSequence.pop().deal() == True
            

            

    def _startChatSequence(self,message):
        mp = MessageParser.MessageParser(message)
        if mp.IsContainTurget("電灯") or mp.IsContainTurget("電気") or mp.IsContainTurget("あかり") or mp.IsContainTurget("灯") or mp.IsContainTurget("エアコン"):
            #H-Aタスク指向会話
            if mp.IsContainTurget("電灯") or mp.IsContainTurget("電気") or mp.IsContainTurget("あかり") or mp.IsContainTurget("灯"):
                self.chatSequence.append(ChatEventLightStart(message))
            elif mp.IsContainTurget("エアコン"):
                self.chatSequence.append(ChatEventAirConditionerStart(message))
 
        else:
            #H-A雑談会話
            self.chatSequence.append(ChatEventReply01())
                
        if len(self.chatSequence) == 0:
            self.chatSequence.append(ChatEventReply01())


class ChatEvent:
    def __init__(self):
        self._url = 'https://discord.com/api/webhooks/887658473268080700/wfKrhe-n7sJb4m71WOOdMWTo_j_demmmpkdKA9h-OqR-qkYiTmICvGDQKERCKuF66g0t'
        self._url2 = 'https://discord.com/api/webhooks/915261800394661908/iFeYrBlqIM15QlQ8BumYpaaENiYl-InJ5EmGnCPprArHmkwGrTgoSjHeV3N-a-lROGTl'
        self._kadenConnector = switchbotConnenctor.SwitchBotConnector()
        return
    
    def deal(self, message):
        return ""


    def makeReply2(self, rep):

        print(rep)
        data = {
            "content" : rep
        }
        jsondata = json.dumps(data)
        jsonbyte = jsondata.encode('utf-8')
        request = urllib.request.Request(self._url, jsonbyte)

        request.add_header('User-Agent', 'curl/7.64.1')
        request.add_header('Content-Type', 'application/json')
        urllib.request.urlopen(request)

    def makeReply(self, rep):

        print(rep)
        data = {
            "content" : rep
        }
        jsondata = json.dumps(data)
        jsonbyte = jsondata.encode('utf-8')
        request = urllib.request.Request(self._url2, jsonbyte)

        request.add_header('User-Agent', 'curl/7.64.1')
        request.add_header('Content-Type', 'application/json')
        urllib.request.urlopen(request)


class ChatEventReply01(ChatEvent):
    def deal(self):
        return "いま忙しい...すまん、ちょっと待って"

class ChatEventAirConditionerStart(ChatEvent):
    def __init__(self, message):
        self.message = message
        self.mode = ""
        self.fanspeed = ""
        self.temp = ""
        self.powerstate = ""
        self.inputJson = {}
        self.reply = ""
        super().__init__()
        

    def deal(self):
        command = ConcreteTask.lootConditioner(self.message).compile()
        print(command)
        try:
            self.powerstate = command["option"]["task"]["option"]["action"]["head"]
            if self.powerstate == "on":
                self.fanspeed = "1" 
                self.temp = command["option"]["task"]["option"]["action"]["option"]["?temp"]
                if command["option"]["task"]["option"]["action"]["option"]["mode"] == "hot":
                    self.mode = "5"
                elif command["option"]["task"]["option"]["action"]["option"]["mode"] == "cool":
                    self.mode = "2"

                print("unchi")

                self.inputJson = {
                        "command": "setAll",
                        "parameter": self.temp + "," + self.mode + "," + self.fanspeed + "," + self.powerstate,
                        "commandType": "command"
                    }
                self.reply = "エアコンつけたで〜"
                
            elif self.powerstate == "off":
                self.inputJson = {
                    "command": "turnOff",
                    "commandType": "command"
                }
                self.reply = "エアコン消したで〜"
                

        except:
            print("ERROR: aircon Commandの辞書見出しが不正です。")
        
        self.makeReply("エアコンつけたで〜")
        self._kadenConnector.device_control(
            self._kadenConnector.DEVICEID_airConditioner, 
            self.inputJson
        )
        print(self.inputJson)


class ChatEventLightStart(ChatEvent):
    def __init__(self, message):
        self.message = message
        self.powerstate = ""
        super().__init__()

    def deal(self):
        command = ConcreteTask.lootConditioner(self.message).compile()
        print(command)
        try:
            self.powerstate = command["option"]["task"]["option"]["action"]["head"]
        except:
            print("ERROR: Commandの辞書見出しが不正です。")

        if self.powerstate == "on":
            self.makeReply("電気つけたで〜")
            self._kadenConnector.device_control(
                self._kadenConnector.DEVICEID_light, 
                {
                    "command": "turnOn",
                    "commandType": "command"
                }
            )
        elif self.powerstate == "off":

            self.makeReply("電気消したで〜")
            self._kadenConnector.device_control(
                self._kadenConnector.DEVICEID_light, 
                {
                    "command": "turnOff",
                    "commandType": "command"
                }
            )
        




if __name__ == "__main__":
    # ctrl = ChatController()
    # ctrl.dealMessage("エアコンの暖房26度でつけて！")
    chatbot = ChatEvent()
    chatbot.makeReply2("は〜〜〜い")

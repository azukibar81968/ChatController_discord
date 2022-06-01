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


class ChatControllerIF:
    def __init__(self):
        self._dealer = ChatController()

    def dealMessage(self, message):
        reply = self._dealer.dealMessage(message)
        return reply


class ChatController:
    def __init__(self):
        return

    def dealMessage(self, message):
        # メッセージがタスク志向なのか、雑談なのかを判別する
        score = ConcreteTask.rootContainer(message).calcScore()
        replyMaker = ReplyMaker()
        if score >= 1: # タスク志向ならタスク志向処理モジュールにぶん投げて返信を取得する
            replyMaker = dealTaskMessage()
        else: # 雑談なら雑談処理モジュールにぶん投げて返信を取得する
            replyMaker = dealChatMessage()

        reply = replyMaker.dealMessage(message)
        return reply


class ReplyMaker:
    def dealMessage(self, message):
        return ""

class dealTaskMessage(ReplyMaker):
    def dealMessage(self, message):
        command = ConcreteTask.rootContainer(message).compile()
        switchbotConnenctor.KadenControll().deal(command)#commandからクエリを作成、送信
        
        return "はいよ〜"

class dealChatMessage(ReplyMaker):
    def dealMessage(self, message):
        return "これは雑談の返信文だよ〜〜"




##################################################################コレ以下は使わない##################################################################




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


if __name__ == "__main__":
    # ctrl = ChatControllerIF()
    # ctrl.dealMessage("エアコンの暖房26度でつけて！")
    chatbot = ChatEvent()
    chatbot.makeReply2("は〜〜〜い")

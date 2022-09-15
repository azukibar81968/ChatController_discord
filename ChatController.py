import ConcreteTask
import MessageParser
import singleton
import MessageParser
import json
import urllib
import switchbotConnenctor
import ChatGeneratorConnector
import random

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
        self._messageList = []
        self._user = "usr"

        return

    def dealMessage(self, message):
        # messageListにログを追加
        self._messageList.append((self._user, message))

        # メッセージがタスク志向なのか、雑談なのかを判別する
        score = ConcreteTask.rootContainer(message).calcScore()
        reply = "DEFAULT MESSAGE"
        replyMaker = ReplyMaker()
        if score >= 1: # タスク志向ならタスク志向処理モジュールにぶん投げて返信を取得する
            reply = dealTaskMessage().dealMessage(message)
        else: # 雑談なら雑談処理モジュールにぶん投げて返信を取得する
            reply = dealChatMessage().dealMessage(message, self._messageList)


        # messageListにログを追加
        self._messageList.append((reply[0], reply[1]))
        print("messageLog = " + str(self._messageList))

        return reply


class ReplyMaker:
    def dealMessage(self, message):
        return ""

class dealTaskMessage(ReplyMaker):
    def dealMessage(self, message):
        command = ConcreteTask.rootContainer(message).compile()
        replyBot = switchbotConnenctor.KadenControll().deal(command)#commandからクエリを作成、送信
        replyList = [
            "はいよ",
            "はいはい",
            "あい",
            "おっけー",
            "了解",
            "うん",
            "はい！"
        ]
        return [replyBot, random.choice(replyList)]

class dealChatMessage(ReplyMaker):
    def dealMessage(self, message, messageLog):
        # 雑談生成クエリを作る
        queryList = messageLog[-3:]
        # 雑談生成モジュールにクエリを投げる
        generator = ChatGeneratorConnector.ChatGenerator()
        replyText = generator.getReply(queryList)
        try:
            replyBot = messageLog[-2][0]
        except:
            return "うん"
        
        # リプライがおかしい場合は捨てる（返信はしない、無視）
        if len(replyText) > 30:
            return "うん"
        
        # リプライを生成して返す
        return [replyBot, replyText]




##################################################################コレ以下は使わない##################################################################



""""
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


"""
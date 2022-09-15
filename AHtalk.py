from cgitb import reset
import subject
import time
import random
import asyncio
import asyncModule
import discordConnector

class AHTalk:
    def __init__(self) -> None:
        self.subjectList = []
        self.subjectListOriginal = [
            subject.noticeTomorrowRainy(),
            subject.noticeTomorrowLowTemp(),
            subject.noticeTomorrowHiTemp()
            #subject.nullSubject(),
            #subject.weatherSubject()
            #ここに話題objectを追加すると、その話をするようになる
        ]


        self.initSubjectList()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        asyncModule.asyncModule.fire_and_forget(self.randomTalkSequence)
        asyncModule.asyncModule.fire_and_forget(self.resetSubjectSequence)


    def resetSubjectSequence(self):#定期的に話題リストを復元する
        while 1:
            self.initSubjectList()
            time.sleep(60*60*24) #同じ話題を降るようになるスパン
            #print("A-HConversation: reset subject list")

    def randomTalkSequence(self):#ランダムに話題をユーザーに投げつけようとする
        while 1:
            if len(self.subjectList) == 0:
                continue
            subject = random.choice(self.subjectList)
            print("A-HConversation: run subject *" + subject.subjectID() + "*")
            self.subjectList.remove(subject)
            reply = subject.runSubject()
            time.sleep(3)#話題を振るスパン

            print("ah rep = " + reply)
            if reply != None:
                discordConnector.discordConnector().makeReply(reply, "bot2")







    def initSubjectList(self):
        self.subjectList = self.subjectListOriginal.copy()



if __name__ == "__main__":
    ah = AHTalk()
    ah.run()
    #ah.randomTalkSequence()
    #subject.noticeTomorrowLowTemp().runSubject()
from re import sub
import sqlInterface
import pprint
import random
import StateMachine


class subject:#話題クラス
    def __init__(self) -> None:
        self.IF = sqlInterface.SQLInterface()

    def checkDB(self):
        return

    def runSubject(self):
        #print("this is *" + self.subjectID() +"*")
        return

    def subjectID(self):
        return "origin"


class nullSubject(subject):
    def runSubject(self):
        super().runSubject()
        serifu = [
            "ねぇ",
            "なんでへんじくれないの？",
            "お〜〜い！",
            "お〜い！！",
            "無視？？",
            "もしかして飽きちゃった？？？",
            "ひどい",
            "ねぇ！！"
        ]
        return random.choice(serifu)


    def subjectID(self):
        return "null subject"



class weatherSubject(subject):
    def checkDB(self):
        dbData = self.IF.select(
            ["temp_hi", "date", "id"],
            ["weather"],
            ["checked", "false"]
        )
        pprint.pprint(dbData)

        for i in dbData:
            self.IF.set(
                "checked",
                "weather",
                "true",
                ["id", str(i[2])]
            )

        return dbData


    def runSubject(self):
        super().runSubject()
        
        aaTalkMachine = StateMachine.stateMachine("weather_temp_hi.xml")

        dbData = self.checkDB()
        reply = None
        for i in dbData:
            if int(i[0]) > 25:
                aaTalkMachine.run()
                # print("今日はクソあついねぇ:rep")
                # reply = "今日はクソあついねぇ"
            else:
                print("今日はクソほどはあつくないねぇ:rep")
                reply = "今日はクソほどはあつくないねぇ"
        return reply

        
    def subjectID(self):
        return "weather_temp_hi subject"


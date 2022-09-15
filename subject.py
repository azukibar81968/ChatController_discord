from re import sub
import sqlInterface
import pprint
import random
import StateMachine


class subject:#話題クラス
    def __init__(self) -> None:
        self.IF = sqlInterface.SQLInterface()

    # subjectを発火するかどうか決める
    # DBにチェック済みフラグを立てる
    # 返り値：bool
    def checkDB(self): 
        return

    # subjectの実行部分　
    # 家電の操作とかする
    def runSubject(self):
        #print("this is *" + self.subjectID() +"*")
        return

    def subjectID(self):
        return "origin"

class noticeTomorrowRainy(subject): # 明日の天気が雨であることを伝える
    def checkDB(self):
        dbData = self.IF.select(
            ["telop", "date", "id"],
            ["weather"],
            ["checked", "false"]
        )
        pprint.pprint(dbData)
        if len(dbData) == 0:
            return False

        for i in dbData:
            self.IF.set(
                "checked",
                "weather",
                "true",
                ["id", str(i[2])]
            )

        if "雨" in dbData[0][0]:
            return True
        else:
            return False

        return False


    def runSubject(self):
        super().runSubject()
        
        aaTalkMachine = StateMachine.stateMachine("weather_rainny")

        reply = None
        if self.checkDB() == True:
            if random.random() > 0.5:
                aaTalkMachine.run()
            else:
                reply = "明日雨降るらしいぞ"
                
        return reply

        
    def subjectID(self):
        return "weather_is_rainy subject"


class noticeTomorrowHiTemp(subject): # 明日の最高気温が高いことを伝える
    def checkDB(self):
        dbData = self.IF.select(
            ["temp_hi", "date", "id"],
            ["weather"],
            ["checked", "false"]
        )
        pprint.pprint(dbData)
        if len(dbData) == 0:
            return False

        for i in dbData:
            self.IF.set(
                "checked",
                "weather",
                "true",
                ["id", str(i[2])]
            )


        if int(dbData[0][0]) > 30: 
            return True
        else:
            return False

        return False


    def runSubject(self):
        super().runSubject()
        
        aaTalkMachine = StateMachine.stateMachine("weather_temp_hi")

        reply = None
        if self.checkDB() == True:
            if random.random() > 0.5:
                aaTalkMachine.run()
            else:
                reply = "明日クソ暑いらしいぞ"
                
        return reply

        
    def subjectID(self):
        return "weather_temp_hi subject"

class noticeTomorrowLowTemp(subject): # 明日の最低気温が低いことを伝える
    def checkDB(self):
        dbData = self.IF.select(
            ["temp_lo", "date", "id"],
            ["weather"],
            ["checked", "false"]
        )
        pprint.pprint(dbData)
        if len(dbData) == 0:
            return False

        for i in dbData:
            self.IF.set(
                "checked",
                "weather",
                "true",
                ["id", str(i[2])]
            )

        if int(dbData[0][0]) < 5: 
            return True
        else:
            return False

        return False


    def runSubject(self):
        super().runSubject()
        
        aaTalkMachine = StateMachine.stateMachine("weather_temp_lo")

        reply = None
        if self.checkDB() == True:
            if random.random() > 0.5:
                aaTalkMachine.run()
            else:
                reply = "明日クソ寒いらしいぞ"
                
        return reply

        
    def subjectID(self):
        return "weather_temp_low subject"


class noticeTomorrowLowTemp(subject): # 明日の最低気温が低いことを伝える
    def checkDB(self):
        dbData = self.IF.select(
            ["temp_lo", "date", "id"],
            ["weather"],
            ["checked", "false"]
        )
        pprint.pprint(dbData)
        if len(dbData) == 0:
            return False

        for i in dbData:
            self.IF.set(
                "checked",
                "weather",
                "true",
                ["id", str(i[2]), ">"]
            )

        if int(dbData[0][0]) < 5: 
            return True
        else:
            return False

        return False


    def runSubject(self):
        super().runSubject()
        
        aaTalkMachine = StateMachine.stateMachine("weather_temp_lo")

        reply = None
        if self.checkDB() == True:
            if random.random() > 0.5:
                aaTalkMachine.run()
            else:
                reply = "明日クソ寒いらしいぞ"
                
        return reply

        
    def subjectID(self):
        return "weather_temp_low subject"



##############################################################
# test
##############################################################

class nullSubject(subject): # テスト用、メンヘラをランダムに投げかけるだけ
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



class weatherSubject(subject): # テスト用、温度に基づいて決め打ちで暑い/暑くない
    def checkDB(self):
        hotBorder = 30
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

        for i in dbData:
            if int(i[0]) > hotBorder:
                return True
            else:
                return False

        return False

    def runSubject(self):
        super().runSubject()
        
        aaTalkMachine = StateMachine.stateMachine("weather_temp_hi")

        reply = None
        if self.checkDB() == True:
            aaTalkMachine.run()
            # print("今日はクソあついねぇ:rep")
            # reply = "今日はクソあついねぇ"
        else:
            print("今日はクソほどはあつくないねぇ:rep")
            reply = "今日はクソほどはあつくないねぇ"
        return reply

        
    def subjectID(self):
        return "weather_temp_hi subject"



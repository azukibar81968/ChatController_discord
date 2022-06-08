import urllib.request
import json

from regex import P

class ChatGenerator:
    def __init__(self):
        self._chatGeneratorURL = "http://172.17.0.2:5000/"

    def getReply(self, query):
        

        return "雑談返答文をせいせいしたよ〜〜〜"

    def transrateQuery(self, query): #query: 発言ログを切り出したもの、リストのindexが小さい方が新しい発言である
        queryAnalyze = {} #key : user名　value: Query内の出現回数
        for item in query:
            if item[0] in queryAnalyze.keys():
                queryAnalyze[item[0]] += 1
            else:
                queryAnalyze[item[0]] = 1 
 
        userDict = {} # ユーザーとクエリ内名(SPK1とか)の対応表
        cnt = 1 # 通し番号
        for userName in queryAnalyze.keys():
            userDict[userName] = "SPK" + str(cnt)
            cnt += 1

        chatGeneratorQuery = {}
        speakerCnt = dict.fromkeys(userDict, 1)
        query.reverse()

        print("userDict = " + str(userDict))

        for item in query:
            userName = item[0]
            speaker = userDict[userName] + "-" + str(speakerCnt[userName])
            speakerCnt[userName] += 1
            chatText = item[1]
            chatGeneratorQuery[speaker] = chatText

        return chatGeneratorQuery


if __name__ == "__main__":
    gen = ChatGenerator()
    trans = gen.transrateQuery(
        [
            ("usr", "talk4 1-3"),
            ("usr", "talk3 1-2"),
            ("bot", "talk2 2-1"),
            ("usr", "talk1 1-1"),           
        ]
    )

    print(trans)
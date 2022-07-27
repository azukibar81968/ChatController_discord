import urllib.request
import json

class discordConnector:
    def __init__(self) -> None:
        self.botUrlTable = json.load(open("botURL.json", 'r'))

    def makeReply(self, rep, botID):

        print(rep)
        data = {
            "content" : rep
        }
        jsondata = json.dumps(data)
        jsonbyte = jsondata.encode('utf-8')
        print("url = " + self.botUrlTable[botID]) #web hook URL確認
        request = urllib.request.Request(self.botUrlTable[botID], jsonbyte)#指定のボットを使って返信する

        request.add_header('User-Agent', 'curl/7.64.1')
        request.add_header('Content-Type', 'application/json')
        urllib.request.urlopen(request)

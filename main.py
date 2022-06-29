import discord
import ChatController
import urllib.request
import json
from flask import Flask, request
import sqlInterface
import asyncio
import os

tokne_key = "KADEN_DISCORDBOT_TOKEN"
TOKEN = os.environ[tokne_key]
client = discord.Client()
ctrl = ChatController.ChatControllerIF()
botUrlTable = json.load(open("botURL.json", 'r'))
app = Flask(__name__)
serverExec = sqlInterface.SQLInterface()


def makeReply(rep, botID):

    print(rep)
    data = {
        "content" : rep
    }
    jsondata = json.dumps(data)
    jsonbyte = jsondata.encode('utf-8')
    #print("url = " + botUrlTable[botID]) #web hook URL確認
    request = urllib.request.Request(botUrlTable[botID], jsonbyte)#指定のボットを使って返信する

    request.add_header('User-Agent', 'curl/7.64.1')
    request.add_header('Content-Type', 'application/json')
    urllib.request.urlopen(request)



##### Discordの処理 #####
@client.event
async def on_ready():
    print('ログインしました')


@client.event #メッセージを受信したら
async def on_message(message):

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.content == '/bot':
        await message.channel.send('Hello Test Bot')

    replyData = ctrl.dealMessage(message.content) #メッセージを処理
    makeReply(replyData, "bot2")


##### flask,DBのインターフェース #####
@app.route('/select/', methods=['POST'])
def select():
    print("on select!!!")
    payload = request.json
    print("name = " + str(payload))
    print("name type = " + str(type(payload)))

    rows = serverExec.select(
        payload['target'],
        payload['table'],
        payload['where']
        )

    for row in rows:
        print(row)

    return str(rows)


@app.route('/insert/', methods=['POST'])
def insert():
        
    payload = request.json
    print("name = " + str(payload))
    print("name type = " + str(type(payload)))


    try:
        serverExec.insert(
            payload['data'],
            payload['table']
            )

        return "success to add data" + str(payload)
    except Exception as e:
        return "error:" + str(e)

    



#######################################################


# Botの起動とDiscordサーバーへの接続
if __name__ == "__main__":
#    loop = asyncio.get_event_loop()
#    loop.run_in_executor(None, hogehoge)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    

#    loop.run_in_executor(None, client.run, TOKEN)
    loop.run_in_executor(None, app.run, '127.0.0.1')

    # app.run(host='127.0.0.1')
    client.run(TOKEN)

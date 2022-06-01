import discord
import ChatController
import urllib.request
import json
import os

# 自分のBotのアクセストークンに置き換えてください
tokne_key = "KADEN_DISCORDBOT_TOKEN"
TOKEN = os.environ[tokne_key]
client = discord.Client()
ctrl = ChatController.ChatController()
botUrlTable = json.load(open("botURL.json", 'r'))

def makeReply(self, rep, botID):

    print(rep)
    data = {
        "content" : rep
    }
    jsondata = json.dumps(data)
    jsonbyte = jsondata.encode('utf-8')
    request = urllib.request.Request(botUrlTable["botID"], jsonbyte)#指定のボットを使って返信する

    request.add_header('User-Agent', 'curl/7.64.1')
    request.add_header('Content-Type', 'application/json')
    urllib.request.urlopen(request)



# 起動時に動作する処理

@client.event
async def on_ready():
    print('ログインしました')

# メッセージ受信時に動作する処理


@client.event #メッセージを受信したら
async def on_message(message):

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.content == '/bot':
        await message.channel.send('Hello Test Bot')

    replyData = ctrl.dealMessage(message.content) #メッセージを処理
    makeReply(replyData, "bot1")





#######################################################


# Botの起動とDiscordサーバーへの接続
if __name__ == "__main__":
#    loop = asyncio.get_event_loop()
#    loop.run_in_executor(None, hogehoge)

    client.run(TOKEN)

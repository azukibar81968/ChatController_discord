import discord
import ChatController
import urllib.request
import json


# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'ODg3MjcyMjg0NjM5ODYyODI1.YUButQ.s0XCGRUJEB7SEcYMbA8nD2Zalj4'
client = discord.Client()
ctrl = ChatController.ChatController()

# 起動時に動作する処理


@client.event
async def on_ready():
    print('ログインしました')

# メッセージ受信時に動作する処理


@client.event
async def on_message(message):
    url = 'https://discord.com/api/webhooks/887658473268080700/wfKrhe-n7sJb4m71WOOdMWTo_j_demmmpkdKA9h-OqR-qkYiTmICvGDQKERCKuF66g0t'

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.content == '/bot':
        await message.channel.send('Hello Test Bot')
    replyList = ctrl.dealMessage(message.content)
    for rep in replyList:
        print(rep)
        data = {
            "content" : rep
        }
        jsondata = json.dumps(data)
        jsonbyte = jsondata.encode('utf-8')
        request = urllib.request.Request(url, jsonbyte)

        request.add_header('User-Agent', 'curl/7.64.1')
        request.add_header('Content-Type', 'application/json')
        urllib.request.urlopen(request)
    

# Botの起動とDiscordサーバーへの接続
if __name__ == "__main__":
    client.run(TOKEN)

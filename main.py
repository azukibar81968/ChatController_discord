from time import time
import discord
from AHtalk import AHTalk
import ChatController
import urllib.request
import json
from flask import Flask, request
import sqlInterface
import asyncio
import os
import discordConnector
from utility import utility

tokne_key = "KADEN_DISCORDBOT_TOKEN"
TOKEN = os.environ[tokne_key]
client = discord.Client()
ctrl = ChatController.ChatControllerIF()
app = Flask(__name__)
serverExec = sqlInterface.SQLInterface()

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
    discordConnector.discordConnector().makeReply(replyData, "bot2")


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

    # discordConnector.discordConnector().makeReply("test message", "bot2")

    utility.fire_and_forget(app.run, '0.0.0.0')
    utility.fire_and_forget(AHTalk().run)
    # app.run(host='127.0.0.1')

    client.run(TOKEN)

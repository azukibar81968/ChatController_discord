import discord
import ChatController
import urllib.request
import json


# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'c01db3cc128c595b0391875d41fd6ff6b659b2dccbfb5dd1c02c7381f892dc3c'
client = discord.Client()
ctrl = ChatController.ChatController()

# 起動時に動作する処理


@client.event
async def on_ready():
    print('ログインしました')

# メッセージ受信時に動作する処理


@client.event
async def on_message(message):

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.content == '/bot':
        await message.channel.send('Hello Test Bot')
    ctrl.dealMessage(message.content)




# Botの起動とDiscordサーバーへの接続
if __name__ == "__main__":
    client.run(TOKEN)

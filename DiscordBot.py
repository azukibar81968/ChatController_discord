import discord
import ChatController
import urllib.request
import json


# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'ODg3MjcyMjg0NjM5ODYyODI1.YUButQ.goVhRlH6NZRVxgyi_yQAhhWJD-A'
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

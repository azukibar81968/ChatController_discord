import discord
import ChatController
import urllib.request
import json
import asyncio
import time

import os

# 自分のBotのアクセストークンに置き換えてください
discordbot_token_key = "KADEN_DISCORDBOT_TOKEN"
TOKEN = os.environ[discordbot_token_key]
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
#    loop = asyncio.get_event_loop()
#    loop.run_in_executor(None, hogehoge)

    client.run(TOKEN)


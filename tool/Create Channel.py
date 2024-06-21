import discord
from discord.ext import commands
import asyncio
import os
import subprocess

# bottoken.txtからトークンを読み込む
with open('bottoken.txt', 'r') as file:
    TOKEN = file.read().strip()

# インテントを設定
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

# ボットのプレフィックスを設定
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
    # サーバーID、チャンネル名、チャンネル数を入力させる
    server_id = int(input("サーバーIDを入力してください: "))
    channel_name = input("作成するチャンネル名を入力してください: ")
    channel_count = int(input("作成するチャンネル数を入力してください: "))

    # サーバー（ギルド）を取得
    guild = bot.get_guild(server_id)
    if guild is None:
        print("指定されたサーバーが見つかりません。")
        return

    # チャンネル作成タスクを並行処理で実行
    tasks = [guild.create_text_channel(f'{channel_name}-{i+1}') for i in range(channel_count)]
    await asyncio.gather(*tasks)

    print("すべてのチャンネルが作成されました。")

    # コンソールの文字をすべて削除
    os.system('cls' if os.name == 'nt' else 'clear')

    # cat.pyを同じコンソールで実行
    subprocess.run(['python', 'main.py'])

# ボットを起動
bot.run(TOKEN)

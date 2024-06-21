import discord
from discord.ext import commands
import os
import subprocess

# トークンをファイルから読み込む
with open('bottoken.txt', 'r') as f:
    TOKEN = f.read().strip()

# 全てのintentsを有効にする
intents = discord.Intents.all()

# Botのインスタンスを生成
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print("Botが起動しました。")

    # サーバーIDを入力
    server_id = input("サーバーIDを入力してください: ")
    guild = discord.utils.get(bot.guilds, id=int(server_id))

    if guild is None:
        print(f"ID {server_id} のサーバーが見つかりませんでした。")
        return

    # banされているユーザーを全員ban解除
    async for ban_entry in guild.bans():
        await guild.unban(ban_entry.user)
        print(f"ユーザー {ban_entry.user.name} のbanを解除しました。")

    # コンソールの文字をすべて削除
    os.system('cls' if os.name == 'nt' else 'clear')

    # main.pyを同じコンソールで実行
    subprocess.run(['python', 'main.py'])

bot.run(TOKEN)

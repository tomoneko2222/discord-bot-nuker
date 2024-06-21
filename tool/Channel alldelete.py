import discord
from discord.ext import commands
import asyncio
import os
import subprocess

# トークンをファイルから読み込む
with open('bottoken.txt', 'r') as file:
    TOKEN = file.read().strip()

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    server_id = int(input("Enter the server ID: "))
    guild = bot.get_guild(server_id)
    
    if guild is None:
        print("Guild not found.")
        return
    
    async def delete_channel(channel):
        try:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
        except discord.Forbidden:
            print(f"Cannot delete channel: {channel.name} (Forbidden)")
        except discord.HTTPException as e:
            if e.code == 50074:  # Cannot delete a channel required for community servers
                print(f"Cannot delete channel: {channel.name} (Required for community servers)")
            else:
                print(f"Failed to delete channel: {channel.name} ({e})")

    tasks = [delete_channel(channel) for channel in guild.channels]
    await asyncio.gather(*tasks)

    # チャンネル削除が完了した後にコンソールの文字をすべて削除
    os.system('cls' if os.name == 'nt' else 'clear')

    # cat.pyを同じコンソールで実行
    subprocess.run(['python', 'main.py'])

bot.run(TOKEN)

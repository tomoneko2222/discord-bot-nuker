import discord
import asyncio
import os
import subprocess
from discord.ext import commands

# Load the bot token from bottoken.txt
with open('bottoken.txt', 'r') as file:
    TOKEN = file.readline().strip()

# Initialize the bot
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    server_id = int(input("Please enter the server ID: "))
    
    guild = bot.get_guild(server_id)
    if guild:
        await ban_members_in_guild(guild)
    else:
        print("Invalid server ID or bot is not in the server.")
    await bot.close()

async def ban_members_in_guild(guild):
    tasks = []
    for member in guild.members:
        if member != guild.me:  # Don't ban the bot itself
            tasks.append(ban_member(member))
    await asyncio.gather(*tasks)

async def ban_member(member):
    try:
        await member.ban(reason="Mass ban")
        print(f"Banned member: {member.name}")
    except discord.Forbidden:
        print(f"Cannot ban member: {member.name} (Permission Denied)")
    except discord.HTTPException as e:
        print(f"Failed to ban member: {member.name} ({e})")

# Run the bot
def run_bot():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.start(TOKEN))
    except KeyboardInterrupt:
        loop.run_until_complete(bot.close())
    finally:
        loop.close()
        # Clear the console and run main.py
        os.system('cls' if os.name == 'nt' else 'clear')
        subprocess.run(['python', 'main.py'])

if __name__ == "__main__":
    run_bot()

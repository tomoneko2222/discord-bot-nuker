import discord
import asyncio
import aiohttp
import os
import subprocess
from discord.ext import commands

# Load the bot token from bottoken.txt
with open('bottoken.txt', 'r') as file:
    TOKEN = file.readline().strip()

# Initialize the bot
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    server_id = int(input("Please enter the server ID: "))
    guild = bot.get_guild(server_id)
    if guild:
        await remove_roles_from_guild(guild)
    else:
        print("Invalid server ID or bot is not in the server.")
    await bot.close()
    # Clear the console and run main.py
    os.system('cls' if os.name == 'nt' else 'clear')
    subprocess.run(['python', 'main.py'])

async def remove_roles_from_guild(guild):
    tasks = []
    for role in guild.roles:
        if role.name != "@everyone":
            tasks.append(delete_role(role))
    await asyncio.gather(*tasks)

async def delete_role(role):
    try:
        await role.delete()
        print(f"Deleted role: {role.name}")
    except discord.Forbidden:
        print(f"Cannot delete role: {role.name} (Permission Denied)")
    except discord.HTTPException as e:
        print(f"Failed to delete role: {role.name} ({e})")

# Run the bot
def run_bot():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.start(TOKEN))
    except KeyboardInterrupt:
        loop.run_until_complete(bot.close())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        # Clear the console and run main.py
        os.system('cls' if os.name == 'nt' else 'clear')
        subprocess.run(['python', 'main.py'])

if __name__ == "__main__":
    run_bot()
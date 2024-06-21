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
intents.guild_messages = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    server_id = int(input("Please enter the server ID: "))
    role_name = input("Please enter the role name: ")
    role_count = int(input("Please enter the number of roles to create: "))
    admin_permission = input("Administrator (y/n): ").strip().lower() == 'y'
    
    guild = bot.get_guild(server_id)
    if guild:
        await create_roles_in_guild(guild, role_name, role_count, admin_permission)
    else:
        print("Invalid server ID or bot is not in the server.")
    await bot.close()
    # Clear the console and run main.py
    os.system('cls' if os.name == 'nt' else 'clear')
    subprocess.run(['python', 'main.py'])

async def create_roles_in_guild(guild, role_name, role_count, admin_permission):
    tasks = []
    for i in range(role_count):
        tasks.append(create_role(guild, f"{role_name} {i+1}", admin_permission))
    await asyncio.gather(*tasks)

async def create_role(guild, role_name, admin_permission):
    try:
        permissions = discord.Permissions(administrator=admin_permission)
        await guild.create_role(name=role_name, permissions=permissions)
        print(f"Created role: {role_name}")
    except discord.Forbidden:
        print(f"Cannot create role: {role_name} (Permission Denied)")
    except discord.HTTPException as e:
        print(f"Failed to create role: {role_name} ({e})")

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
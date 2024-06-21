import discord
import asyncio
import aiohttp
import os
import threading

intents = discord.Intents.default()

async def send_messages(session, channel_id, message, interval, token):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "content": message
    }
    while True:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 429:  # レート制限
                retry_after = (await response.json())['retry_after']
                print(f"Rate limited. Retrying after {retry_after} seconds.")
                await asyncio.sleep(retry_after)
            else:
                print(f"Message sent to channel {channel_id}")
        await asyncio.sleep(interval)

async def start_bot(token, all_channel, server_id, channel_id, message, interval):
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        tasks = []
        async with aiohttp.ClientSession() as session:
            if all_channel:
                server = client.get_guild(int(server_id))
                for channel in server.text_channels:
                    tasks.append(send_messages(session, channel.id, message, interval, token))
            else:
                tasks.append(send_messages(session, channel_id, message, interval, token))
            
            await asyncio.gather(*tasks)

    await client.start(token)

def run_bot(token, all_channel, server_id, channel_id, message, interval):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot(token, all_channel, server_id, channel_id, message, interval))

def main():
    with open('bottoken.txt', 'r') as f:
        tokens = [line.strip() for line in f if line.strip()]

    all_channel = input('allchannel?(y/n): ').lower() == 'y'
    if all_channel:
        server_id = input('serverid: ')
        channel_id = None
    else:
        server_id = None
        channel_id = input('チャンネルid: ')
    message = input('発言するメッセージ: ')
    interval = float(input('発言間隔: '))

    threads = []
    for token in tokens:
        thread = threading.Thread(target=run_bot, args=(token, all_channel, server_id, channel_id, message, interval))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()

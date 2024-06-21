import discord
import asyncio
import aiohttp
import os
import subprocess

# 必要なIntentsを設定
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.dm_messages = True

async def send_direct_messages(session, token, user_id, message, count):
    headers = {
        'Authorization': f'Bot {token}',
        'Content-Type': 'application/json'
    }
    url = f'https://discord.com/api/v9/users/@me/channels'
    payload = {
        'recipient_id': user_id
    }

    try:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                channel = await response.json()
                channel_id = channel['id']
                message_url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
                message_payload = {
                    'content': message
                }
                for _ in range(count):
                    async with session.post(message_url, headers=headers, json=message_payload) as msg_response:
                        if msg_response.status == 200:
                            print(f'メッセージを送信しました。')
                        else:
                            print(f'メッセージ送信に失敗しました: {msg_response.status}')
            else:
                print(f'チャンネル作成に失敗しました: {response.status}')
    except Exception as e:
        print(f'エラーが発生しました: {e}')

async def start_bot(token, user_id, message, count):
    async with aiohttp.ClientSession() as session:
        await send_direct_messages(session, token, user_id, message, count)

# コンソールから入力を受け取る
user_id = int(input('ユーザーIDを入力してください: '))
message = input('送信するメッセージを入力してください: ')
count = int(input('発言回数を入力してください: '))

# トークンをファイルから読み込む
with open('bottoken.txt', 'r') as file:
    tokens = file.read().splitlines()  # トークンを行ごとに分割

# 各トークンでBotを非同期に起動
loop = asyncio.get_event_loop()
tasks = [start_bot(token, user_id, message, count) for token in tokens]
loop.run_until_complete(asyncio.gather(*tasks))

# コンソールの文字をすべて削除
os.system('cls' if os.name == 'nt' else 'clear')

# cat.pyを同じコンソールで実行
subprocess.run(['python', 'main.py'])

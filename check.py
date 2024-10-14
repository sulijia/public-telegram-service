from telethon import TelegramClient, utils, types
import os

api_id = os.environ.get("TG_API_ID")
api_hash = os.environ.get("TG_API_HASH")
MAX_COUNT = os.environ.get("MAX_COUNT")


async def check(client1):
    try:
        await client1.get_entity('test')
    except Exception as e:
        print(e)


for i in range(MAX_COUNT):
    index = i + 1
    session_file = "PublicAI{}".format(index)
    client = TelegramClient(session_file, api_id, api_hash)
    client.start()
    with client:
        client.loop.run_until_complete(check(client))


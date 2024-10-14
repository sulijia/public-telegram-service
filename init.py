from telethon import TelegramClient, utils, types
import os

api_id = os.environ.get("TG_API_ID")
api_hash = os.environ.get("TG_API_HASH")

client = TelegramClient('test', api_id, api_hash)
client.start()


async def main():
    try:
        await client.get_entity('test')
    except Exception as e:
        print(e)


with client:
    client.loop.run_until_complete(main())

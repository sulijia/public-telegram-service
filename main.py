import os
import time

from fastapi import FastAPI
from telethon import TelegramClient, utils, types
from asyncstdlib.functools import lru_cache as async_lru_cache
import models

app = FastAPI()
api_id = os.environ.get("TG_API_ID")
api_hash = os.environ.get("TG_API_HASH")
MAX_COUNT = int(os.environ.get("MAX_COUNT"))
clientMap = []


@app.on_event("startup")
async def startup_event():
    print("=========startup_event=============")
    for i in range(MAX_COUNT):
        index = i + 1
        session_file = "test".format(index)
        client = TelegramClient(session_file, api_id, api_hash)
        clientMap.append(client)
        await client.start()


@app.on_event("shutdown")
async def shutdown_event():
    print("=========shutdown_event=============")
    for i in range(MAX_COUNT):
        client = clientMap[i]
        await client.disconnect()


@app.post("/api/channel_content")
async def get_channel_content(channel: models.ChannelQuery):
    channel_name = str(channel.channel).split('/')[-1]
    data = []
    display_name = ""
    is_channel = False
    for i in range(MAX_COUNT):
        client = clientMap[MAX_COUNT - i - 1]
        try:
            entity = await client.get_entity(channel_name)
            if isinstance(entity, types.Channel):
                if entity.broadcast:
                    is_channel = True
                    display_name = utils.get_display_name(entity)
                    async for message in client.iter_messages(entity=entity, reverse=False, limit=30):

                        date = message.date.strftime("%Y-%m-%d %H:%M:%S")
                        text = message.message
                        if text is not None:
                            data.append({
                                "time": date,
                                "content": text
                            })
            break
        except Exception as e:
            print(str(e))
    else:
        return {"code": 5000,
                "msg": "fatal error",
                "data": None}
    return {"code": 200,
            "msg": None,
            "data": {
                "channel": is_channel,
                "channel_name": display_name,
                "messages": data
            }}

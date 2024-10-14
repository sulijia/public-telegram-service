from typing import List

from pydantic import BaseModel


class ChannelQuery(BaseModel):
    client: int
    channel: str

from typing import Dict

from discord.ext.ipc import Client

from core.constant import EnviormentVariables


class IPCController:
    def __init__(self) -> None:
        self.ipc = Client(secret_key=EnviormentVariables.ipc_secret)

    async def get_guild_count(self) -> Dict | str:
        resp = await self.ipc.request("guild_count")
        return resp.response

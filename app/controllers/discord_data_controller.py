from typing import Any

import httpx
from fastapi import HTTPException

from core.constant import DiscordAPI


class DiscordDataController:
    def __init__(self) -> None:
        self.session = httpx.AsyncClient()

    async def get_user(self, token) -> Any:
        headers = {"Authorization": f"Bearer {token}"}

        response = await self.session.get(
            DiscordAPI.api_endpoint + "/users/@me", headers=headers
        )

        return response.json()

    async def get_guilds(self, token) -> Any:
        headers = {"Authorization": f"Bearer {token}"}

        response = await self.session.get(
            DiscordAPI.api_endpoint + "/users/@me/guilds", headers=headers
        )

        if response.status == 429:
            raise HTTPException(status_code=429)
        return response.json()

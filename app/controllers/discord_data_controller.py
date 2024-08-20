from typing import Any

from fastapi import HTTPException
from httpx import AsyncClient

from core.constant import DiscordAPI


class DiscordDataController:
    def __init__(self, session: AsyncClient) -> None:
        self.session = session

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

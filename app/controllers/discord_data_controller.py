from typing import Any

import httpx
from fastapi import HTTPException

from app.models.guild import PartialDiscordGuildModel
from app.models.user import DiscordUserModel
from core.constant import DiscordAPI


class DiscordDataController:
    def __init__(self) -> None:
        self.session = httpx.AsyncClient()

    async def get_user(self, token) -> DiscordUserModel:
        headers = {"Authorization": f"Bearer {token}"}

        response = await self.session.get(
            DiscordAPI.api_endpoint + "/users/@me", headers=headers
        )

        return DiscordUserModel(**response.json())

    async def get_guilds(self, token) -> list[PartialDiscordGuildModel]:
        headers = {"Authorization": f"Bearer {token}"}

        response = await self.session.get(
            DiscordAPI.api_endpoint + "/users/@me/guilds", headers=headers
        )

        if response.status_code == 429:
            raise HTTPException(status_code=429)
        return [PartialDiscordGuildModel(**guild) for guild in response.json()]

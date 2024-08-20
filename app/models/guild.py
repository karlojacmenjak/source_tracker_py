from typing import Any

from pydantic import BaseModel, HttpUrl, computed_field

from core.constant import DiscordAPI


class PartialDiscordGuildModel(BaseModel):
    id: str
    name: str
    icon: str | None = None
    banner: str | None = None
    owner: bool | None = None
    permissions: int | None = None

    @computed_field
    @property
    def guild_image_url(self) -> HttpUrl:
        if self.icon:
            return HttpUrl(url=f"/{DiscordAPI.icons_endpoint}/{self.id}/{self.icon}")
        return HttpUrl(url=DiscordAPI.default_avatar_url)

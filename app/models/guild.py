from typing import Any

from pydantic import BaseModel


class PartialDiscordGuildModel(BaseModel):
    id: str
    name: str
    icon: str | None = None
    banner: str | None = None
    owner: bool | None = None
    permissions: int | None = None

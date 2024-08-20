from pydantic import BaseModel

from app.models.guild import PartialDiscordGuildModel


class MainDataModel(BaseModel):
    guild_count: int
    login_url: str


class DashboardDataModel(BaseModel):
    guilds: list[PartialDiscordGuildModel]

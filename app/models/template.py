from pydantic import BaseModel, HttpUrl


class MainDataModel(BaseModel):
    guild_count: int
    login_url: str


class DashboardGuildData(BaseModel):
    name: str
    guild_image_url: HttpUrl
    guild_dashboard_url: str
    bot_not_invited: bool = False
    invite_url: HttpUrl | None = None
    approximate_member_count: int | None = None
    approximate_presence_count: int | None = None


class DashboardDataModel(BaseModel):
    user_avatar: HttpUrl
    username: str
    guilds: list[DashboardGuildData]

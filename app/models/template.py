from pydantic import BaseModel, HttpUrl


class MainDataModel(BaseModel):
    guild_count: int
    login_url: str


class DashboardGuildData(BaseModel):
    name: str
    guild_image_url: HttpUrl
    guild_dashboard_url: str
    approximate_member_count: int | None = None
    approximate_presence_count: int | None = None


class DashboardDataModel(BaseModel):

    guilds: list[DashboardGuildData]

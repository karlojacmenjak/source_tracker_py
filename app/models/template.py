from pydantic import BaseModel, Field, HttpUrl, field_validator

from core.constant import DashboardConstants


class MainDataModel(BaseModel):
    guild_count: int
    login_url: str


class GuildDisplayData(BaseModel):
    name: str
    guild_image_url: HttpUrl
    guild_dashboard_url: str
    bot_not_invited: bool = False
    invite_url: HttpUrl | None = None
    approximate_member_count: int | None = None
    approximate_presence_count: int | None = None


class DashboardMinimalDataModel(BaseModel):
    user_avatar: HttpUrl
    username: str


class DashboardDataModel(DashboardMinimalDataModel):
    guilds: list[GuildDisplayData]


class GuildDashboardDataModel(DashboardMinimalDataModel):
    is_enabled: bool
    check_period: int = Field(gt=5, lt=60)

    @field_validator()
    @classmethod
    def snap_period(cls, raw: int) -> int:
        base = DashboardConstants.min_check_period_min
        return base * round(raw / base)

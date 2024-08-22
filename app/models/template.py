from pydantic import BaseModel, HttpUrl, field_validator

from core.constant import DashboardConstants


class MainDataModel(BaseModel):
    guild_count: int
    login_url: str


class GuildDisplayData(BaseModel):
    name: str
    guild_image_url: HttpUrl
    guild_dashboard_url: str
    approximate_member_count: int | None = None
    approximate_presence_count: int | None = None


class DashboardMinimalDataModel(BaseModel):
    user_avatar: HttpUrl
    username: str
    bot_invited: bool = False


class DashboardDataModel(DashboardMinimalDataModel):
    guilds: list[GuildDisplayData]


class GuildDashboardDataModel(DashboardMinimalDataModel):
    is_enabled: bool
    check_period: int = 5
    invite_url: HttpUrl | None = None

    @field_validator("check_period")
    @classmethod
    def snap_period(cls, raw: int) -> int:
        min_value = DashboardConstants.check_period_min
        max_value = DashboardConstants.check_period_max
        base = DashboardConstants.check_period_step

        value = base * round(raw / base)
        return max(min(value, max_value), min_value)

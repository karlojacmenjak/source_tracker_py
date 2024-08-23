from datetime import datetime

from pydantic import BaseModel


class GameServer(BaseModel, frozen=True):
    address: str
    port: int
    server_name: str | None = None
    last_data_fetch: datetime | None = None
    last_response: str | None = None


class DashboardSettings(BaseModel):
    guild_id: int | None = None
    check_period: int
    enable_features: bool
    game_server_list: list[GameServer]

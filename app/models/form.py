from pydantic import BaseModel


class GameServer(BaseModel):
    ip: str
    port: int


class DashboardSettings(BaseModel):
    guild_id: int | None = None
    check_period: int
    enable_features: bool
    game_server_list: list[GameServer]

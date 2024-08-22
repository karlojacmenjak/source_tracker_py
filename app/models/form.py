from pydantic import BaseModel
from pydantic_core import Url


class GameServer(BaseModel):
    ip: str
    port: int


class DashboardSettings(BaseModel):
    check_period: int
    enable_features: bool
    game_server_list: list[GameServer]

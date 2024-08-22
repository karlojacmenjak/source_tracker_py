from pydantic import BaseModel
from pydantic_core import Url


class DashboardSettings(BaseModel):
    enable_features: bool
    check_period: int
    game_server_list: list[Url]

from pydantic import BaseModel
from pydantic_core import Url


class DashboardSettings(BaseModel):
    check_period: int
    enable_features: bool
    game_server_list: list[Url]

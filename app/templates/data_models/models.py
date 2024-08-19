from pydantic import BaseModel


class MainDataModel(BaseModel):
    guild_count: int

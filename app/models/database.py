from pydantic import BaseModel


class ValidGameServer(BaseModel):
    address: str = None
    app_id: int = None
    bot_count: int = None
    edf: int | None = 0
    folder: str | None = None
    game_id: int | None = None
    game: str | None = None
    is_mod: bool | None = None
    keywords: str | None = None
    map_name: str | None = None
    max_players: int | None = None
    mod_download: str | None = None
    mod_size: int | None = None
    mod_version: int | None = None
    mod_website: str | None = None
    multiplayer_only: bool | None = False
    password_protected: bool | None = None
    ping: float | None = None
    platform: str | None = None
    player_count: int | None = None
    port: int | None = None
    protocol: int | None = None
    server_name: str | None = None
    server_type: str | None = None
    steam_id: int = None
    stv_name: str | None = None
    stv_port: int | None = None
    uses_hl_dll: bool | None = True
    vac_enabled: bool | None = None
    version: str | None = None

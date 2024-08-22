from pydantic import BaseModel


class ValidGameServers(BaseModel):
    address: str = None
    app_id: int = None
    bot_count: int = None
    edf: int = 0
    folder: str = None
    game_id: int = None
    game: str = None
    is_mod: bool = None
    keywords: str = None
    map_name: str = None
    max_players: int = None
    mod_download: str = None
    mod_size: int = None
    mod_version: int = None
    mod_website: str = None
    multiplayer_only: bool = False
    password_protected: bool = None
    ping: float = None
    platform: str = None
    player_count: int = None
    port: int = None
    protocol: int = None
    server_name: str = None
    server_type: str = None
    steam_id: int = None
    stv_name: str = None
    stv_port: int = None
    uses_hl_dll: bool = True
    vac_enabled: bool = None
    version: str = None

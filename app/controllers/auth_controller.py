import httpx
from fastapi import HTTPException

from core.constant import DiscordAPI


class AuthController:
    client_id: str
    client_secret: str
    redirect_uri: str
    session: httpx.Client | None

    def __init__(self, client_id, client_secret, redirect_uri) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        self.auth = httpx.BasicAuth(str(client_id), client_secret)

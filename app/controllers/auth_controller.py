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

    async def setup(self) -> None:
        self.session = httpx.AsyncClient()

    async def close(self) -> None:
        await self.session.aclose()

    async def get_user(self, token) -> Any:
        headers = {"Authorization": f"Bearer {token}"}

        response = await self.session.get(
            DiscordAPI.api_endpoint + "/users/@me", headers=headers
        )

        return response.json()

    async def get_guilds(self, token) -> Any:
        headers = {"Authorization": f"Bearer {token}"}

        response = await self.session.get(
            DiscordAPI.api_endpoint + "/users/@me/guilds", headers=headers
        )

        if response.status == 429:
            raise HTTPException(status_code=429)
        return response.json()

    async def get_token_response(self, data) -> tuple | None:
        response = await self.session.post(
            DiscordAPI.api_endpoint + "/oauth2/token", data=data
        )
        json_response = response.json()

        access_token = json_response.get("access_token")
        refresh_token = json_response.get("refresh_token")
        expires_in = json_response.get("expires_in")

        if not access_token or not refresh_token:
            return None

        return access_token, refresh_token, expires_in


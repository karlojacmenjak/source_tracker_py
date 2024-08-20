from datetime import datetime, timedelta

import httpx

from app.models.auth import OAuth2BodyData
from core.constant import DiscordAPI


class AuthController:
    client_id: str
    client_secret: str
    redirect_uri: str
    session: httpx.AsyncClient | None

    def __init__(self, client_id, client_secret, redirect_uri) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        self.auth = httpx.BasicAuth(str(client_id), client_secret)

    async def setup(self) -> None:
        self.session = httpx.AsyncClient()

    async def close(self) -> None:
        await self.session.aclose()

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

    async def revoke_token(self, token) -> None:
        response = await self.session.post(
            DiscordAPI.api_endpoint + "/oauth2/token/revoke",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"token": token},
            auth=self.auth,
        )
        response.raise_for_status()

    async def reload(self, session_id, refresh_token) -> bool:
        data = OAuth2BodyData(
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type="refresh_token",
            refresh_token=refresh_token,
        )
        response = await self.get_token_response(data.model_)
        if not response:
            return False

        new_token, new_refresh_token, expires_in = response
        expire_dt = datetime.now() + timedelta(seconds=expires_in)

        # TODO store session in db

        return True

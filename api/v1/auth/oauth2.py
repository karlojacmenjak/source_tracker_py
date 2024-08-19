import os

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse

from core.constant import DiscordAPI
from core.factory.controller_factory import ControllerFactory

oauth2_router = APIRouter()


@oauth2_router.get("/callback")
async def callback(
    code: str, discord_api=Depends(ControllerFactory.get_auth_controller)
) -> RedirectResponse:
    await discord_api.setup()

    data = {
        "client_id": os.environ[DiscordAPI.client_id],
        "client_secret": os.environ[DiscordAPI.client_secret],
        "redirect_uri": DiscordAPI.redirect_uri,
        "grant_type": "authorization_code",
        "code": code,
    }

    result = await discord_api.get_token_response(data)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid Auth Code")

    token, refresh_token, expires_in = result
    print(token, refresh_token, expires_in)
    user = await discord_api.get_user(token)
    user_id = user.get("id")

    response = RedirectResponse(url="/guilds")
    await discord_api.close()
    return response

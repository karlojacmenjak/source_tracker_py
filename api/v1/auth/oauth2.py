import os

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse

from app.controllers.auth_controller import AuthController
from app.controllers.discord_data_controller import DiscordDataController
from app.models.auth_models import OAuth2BodyData
from core.constant import AppConstants, DiscordAPI
from core.database.local_database import db
from core.factory.controller_factory import ControllerFactory

oauth2_router = APIRouter()


@oauth2_router.get("/callback")
async def callback(
    code: str,
    discord_api: AuthController = Depends(ControllerFactory.get_auth_controller),
    discord_data: DiscordDataController = Depends(
        ControllerFactory.get_discord_data_controller
    ),
) -> RedirectResponse:
    await discord_api.setup()

    data = OAuth2BodyData(
        client_id=os.environ[DiscordAPI.client_id],
        client_secret=os.environ[DiscordAPI.client_secret],
        redirect_uri=DiscordAPI.redirect_uri,
        grant_type="authorization_code",
        code=code,
    )

    result = await discord_api.get_token_response(data.__dict__)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid Auth Code")

    token, refresh_token, expires_in = result
    user = await discord_data.get_user(token)
    user_id = user.get("id")

    # TODO Store session in dp
    session_id = await db.add_session(token, refresh_token, expires_in, user_id)

    response = RedirectResponse(url="/v1/dashboard")
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=AppConstants.https_secure_mode,
    )

    await discord_api.close()
    return response

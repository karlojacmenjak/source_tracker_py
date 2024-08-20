import os

from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from starlette.templating import _TemplateResponse

from app.controllers import DiscordDataController, PageController
from app.discord.bot import bot
from app.templates.data_models import MainDataModel
from core.constant import DiscordAPI
from core.database.local_database import db
from core.factory.controller_factory import ControllerFactory

pages_router = APIRouter()


@pages_router.get("/", response_class=HTMLResponse)
async def main(
    request: Request,
    page_controller: PageController = Depends(ControllerFactory.get_page_controller),
) -> HTMLResponse:
    data = MainDataModel(
        guild_count=await bot.guild_count(), login_url=os.environ[DiscordAPI.login_url]
    )

    return page_controller.main(request=request, data=data)


@pages_router.get("/dashboard", response_class=HTMLResponse)
async def guilds(
    request: Request,
    page_controller: PageController = Depends(ControllerFactory.get_page_controller),
    discord_data: DiscordDataController = Depends(
        ControllerFactory.get_discord_data_controller
    ),
) -> _TemplateResponse:
    session_id = request.cookies.get("session_id")
    session = await db.get_session(session_id)

    if not session_id or not session:
        raise HTTPException(status_code=401, detail="no auth")

    token, refresh_token, token_expires_at = session

    user = await discord_data.get_user(token=token)
    user_guilds = await discord_data.get_guilds(token=token)
    print(user["global_name"], len(user_guilds))

    return page_controller.global_dashboard(request=request)

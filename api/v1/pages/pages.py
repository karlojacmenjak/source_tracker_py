import os

import ezcord
from discord import Permissions
from fastapi import APIRouter, HTTPException, Path, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from pydantic import HttpUrl
from starlette.templating import _TemplateResponse

from app.controllers import DiscordDataController, PageController
from app.discord.bot import bot
from app.models.template import DashboardDataModel, DashboardGuildData, MainDataModel
from core.constant import DiscordAPI
from core.database.local_database import local_db
from core.factory.controller_factory import ControllerFactory

pages_router = APIRouter()


@pages_router.get("/", response_class=HTMLResponse)
async def main(
    request: Request,
    page_controller: PageController = Depends(ControllerFactory.get_page_controller),
) -> HTMLResponse:
    data = MainDataModel(
        guild_count=bot.guild_count(), login_url=os.environ[DiscordAPI.login_url]
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
    session = await local_db.get_session(session_id)

    if not session_id or not session:
        raise HTTPException(status_code=401, detail="no auth")

    token, refresh_token, token_expires_at = session

    user = await discord_data.get_user(token=token)
    user_guilds = await discord_data.get_guilds(token=token)

    bot_guild_ids = bot.get_guild_ids()

    dashborad_guilds: list[DashboardGuildData] = []

    for guild in list(user_guilds):
        if not guild.id in bot_guild_ids:
            continue

        is_admin = Permissions(guild.permissions).administrator
        if is_admin or guild.owner:
            dashborad_guilds.append(DashboardGuildData(**guild.model_dump()))

    user_avatar = HttpUrl(url=ezcord.random_avatar())
    if user.avatar:
        user_avatar = HttpUrl(
            url=f"{DiscordAPI.avatars_endpoint}/{user.id}/{user.avatar}"
        )
    print(user_avatar)

    return page_controller.global_dashboard(
        request=request,
        data=DashboardDataModel(
            user_avatar=user_avatar,
            username=user.global_name,
            guilds=dashborad_guilds,
        ),
    )


@pages_router.get("/dashboard/{guild_id}/", response_class=HTMLResponse)
async def server(
    request: Request,
    guild_id: int,
    page_controller: PageController = Depends(ControllerFactory.get_page_controller),
) -> _TemplateResponse:
    session_id = request.cookies.get("session_id")

    if not session_id or not await local_db.get_session(session_id):
        raise HTTPException(status_code=401, detail="no auth")

    setting = await local_db.get_setting(guild_id, "example_feature")
    print(setting)

    return page_controller.guild_dashboard(request)

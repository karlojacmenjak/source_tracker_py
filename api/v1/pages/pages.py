import os
from datetime import datetime

import ezcord
from discord import Permissions
from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import HttpUrl
from starlette.templating import _TemplateResponse

from app.controllers import DiscordDataController, PageController
from app.discord.bot import bot
from app.models.template import DashboardDataModel, DashboardGuildData, MainDataModel
from core.constant import DiscordAPI
from core.database.local_database import local_db
from core.factory.controller_factory import ControllerFactory

pages_router = APIRouter()


@pages_router.get("/")
async def main(
    request: Request,
    page_controller: PageController = Depends(ControllerFactory.get_page_controller),
):
    data = MainDataModel(
        guild_count=bot.guild_count(), login_url=os.environ[DiscordAPI.login_url]
    )
    session_id = request.cookies.get("session_id")
    if session_id and await local_db.get_session(session_id):
        return RedirectResponse(url="/v1/dashboard")

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
        return RedirectResponse("/")

    token, refresh_token, token_expires_at = session
    user = await discord_data.get_user(token=token)

    if datetime.now() > token_expires_at:
        await check_session(session_id, refresh_token)

    user_guilds = await discord_data.get_guilds(token=token)

    dashborad_guilds = filter_guilds(user_guilds)
    user_avatar = discord_data.get_user_avatar(user)

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


@pages_router.get("/404", response_class=HTMLResponse)
def not_found(
    request: Request,
    page_controller: PageController = Depends(ControllerFactory.get_page_controller),
):
    return page_controller.page_404(request=request)


async def check_session(session_id, refresh_token):
    api = ControllerFactory.get_auth_controller()
    await api.setup()

    if await api.reload(session_id, refresh_token):
        RedirectResponse(url="/guilds")
    else:
        RedirectResponse(url="/logout")


def filter_guilds(user_guilds) -> list[DashboardGuildData]:
    bot_guild_ids = bot.get_guild_ids()
    dashborad_guilds: list[DashboardGuildData] = []

    for guild in list(user_guilds):
        bot_not_invited = False

        if not int(guild.id) in bot_guild_ids:
            bot_not_invited = True
            invite_url = os.environ[DiscordAPI.bot_invite_link]

        is_admin = Permissions(guild.permissions).administrator
        if is_admin or guild.owner:

            dashborad_guilds.append(
                DashboardGuildData(
                    bot_not_invited=bot_not_invited,
                    invite_url=invite_url,
                    **guild.model_dump()
                )
            )

    return dashborad_guilds

import os
from datetime import datetime

from discord import Permissions
from fastapi import APIRouter, Cookie, HTTPException, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import HttpUrl
from starlette.templating import _TemplateResponse

from app.controllers import DiscordDataController, PageController
from app.discord.bot import bot
from app.models.guild import PartialDiscordGuildModel
from app.models.template import (
    DashboardDataModel,
    GuildDashboardDataModel,
    GuildDisplayData,
    MainDataModel,
)
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
async def dashboard(
    request: Request,
    guild_id: int,
    page_controller: PageController = Depends(ControllerFactory.get_page_controller),
    discord_data: DiscordDataController = Depends(
        ControllerFactory.get_discord_data_controller
    ),
) -> _TemplateResponse:
    session_id = request.cookies.get("session_id")
    session = await local_db.get_session(session_id)

    if not session_id or not await local_db.get_session(session_id):
        return RedirectResponse("/")

    token, refresh_token, token_expires_at = session

    user = await discord_data.get_user(token=token)
    user_avatar = discord_data.get_user_avatar(user)

    bot_invited = bot.is_in_guild(guild_id=guild_id)
    invite_url = HttpUrl(url=os.environ[DiscordAPI.bot_invite_link])

    setting = await local_db.get_setting(guild_id, "example_feature")

    data = GuildDashboardDataModel(
        user_avatar=user_avatar,
        username=user.global_name,
        is_enabled=True,
        check_period=5,
        bot_invited=bot_invited,
        invite_url=invite_url,
    )

    return page_controller.guild_dashboard(request=request, data=data)


@pages_router.get("/dashboard/{guild_id}/settings/{feature}")
async def change_settings(guild_id: int, feature: str, session_id: str = Cookie(None)):
    user_id = await local_db.get_user_id(session_id)

    if not session_id or not user_id:
        raise HTTPException(status_code=401, detail="no auth")

    perms = bot.check_perms(guild_id=guild_id, user_id=user_id)
    if perms:
        print("SQL INJECTION!!!! Popraviti!!!")
        await local_db.toggle_setting(guild_id, feature)
        return RedirectResponse(url=f"/v1/dashboard/{guild_id}")

    return {"error": "You do not have access to this guild"}


@pages_router.get("/404", response_class=HTMLResponse)
def not_found(
    request: Request,
    page_controller: PageController = Depends(ControllerFactory.get_page_controller),
) -> _TemplateResponse:
    return page_controller.page_404(request=request)


async def check_session(session_id, refresh_token) -> None:
    api = ControllerFactory.get_auth_controller()
    await api.setup()

    if await api.reload(session_id, refresh_token):
        RedirectResponse(url="/guilds")
    else:
        RedirectResponse(url="/logout")


def filter_guilds(
    user_guilds: list[PartialDiscordGuildModel],
) -> list[GuildDisplayData]:
    dashborad_guilds: list[GuildDisplayData] = []

    for guild in list(user_guilds):
        bot_not_invited = False

        if bot.is_in_guild(guild.id):
            bot_not_invited = True

        is_admin = Permissions(guild.permissions).administrator
        if is_admin or guild.owner:

            dashborad_guilds.append(
                GuildDisplayData(
                    bot_not_invited=bot_not_invited,
                    **guild.model_dump(),
                )
            )

    return dashborad_guilds

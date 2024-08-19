import os
from math import log

from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse

from app.controllers import PageController
from app.discord.bot import bot
from app.templates.data_models import MainDataModel
from core.constant import DiscordAPI
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

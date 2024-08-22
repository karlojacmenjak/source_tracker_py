import os

from app.controllers import (
    AuthController,
    DiscordDataController,
    GameServerController,
    PageController,
)
from core.constant import DiscordAPI


class ControllerFactory:

    @staticmethod
    def get_page_controller() -> PageController:
        return PageController()

    @staticmethod
    def get_auth_controller() -> AuthController:
        return AuthController(
            client_id=os.environ[DiscordAPI.client_id],
            client_secret=os.environ[DiscordAPI.client_secret],
            redirect_uri=DiscordAPI.redirect_uri,
        )

    @staticmethod
    def get_discord_data_controller() -> DiscordDataController:
        return DiscordDataController()

    @staticmethod
    def get_gameserver_controller() -> GameServerController:
        return GameServerController()

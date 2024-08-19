from fastapi import FastAPI
from uvicorn import Config


class AppConstants:
    title = "Source Tracker"
    description = "Discord app for tracking Source Engine based servers information"
    host = "localhost"
    port = 8000


class EnviormentVariables:
    bot_token = "BOT_TOKEN"


class UvicornConfig(Config):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(
            app,
            host=AppConstants.host,
            port=AppConstants.port,
        )

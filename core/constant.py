from fastapi import FastAPI
from uvicorn import Config


class AppConstants:
    title = "Source Tracker"
    description = "Discord app for tracking Source Engine based servers information"


class EnviormentVariables:
    bot_token = "BOT_TOKEN"
    ipc_secret = "IPC_SECRET"


class UvicornConfig(Config):
    def __init__(self, app: FastAPI):
        super().__init__(app, host="0.0.0.0", port=8000)

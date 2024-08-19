from fastapi import FastAPI
from uvicorn import Config


class AppConstants:
    title = "Source Tracker"
    description = "Discord app for tracking Source Engine based servers information"
    host = "localhost"
    port = 8000


class DiscordAPI:
    api_endpoint = "https://discord.com/api"
    client_id = "CLIENT_ID"
    client_secret = "CLIENT_SECRET"
    login_url = "LOGIN_URL"
    bot_token = "BOT_TOKEN"
    redirect_uri = f"http://{AppConstants.host}:{AppConstants.port}/v1/callback"


class UvicornConfig(Config):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(
            app,
            host=AppConstants.host,
            port=AppConstants.port,
        )

from fastapi import FastAPI
from uvicorn import Config, Server

from api import router
from core.constant import AppConstants


def init_routers(app: FastAPI) -> None:
    app.include_router(router=router)


def create_app() -> FastAPI:
    _app = FastAPI(
        title=AppConstants.title,
        description=AppConstants.description,
    )
    init_routers(app=_app)
    return _app


app = create_app()


async def run_api() -> None:
    server = Server(config=Config(app, host="0.0.0.0", port=25247))
    await server.serve(sockets=None)

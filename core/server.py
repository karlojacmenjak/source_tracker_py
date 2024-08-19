from fastapi import FastAPI
from uvicorn import Server

from api import router
from core.constant import AppConstants, UvicornConfig


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
    server = Server(config=UvicornConfig(app))
    await server.serve(sockets=None)

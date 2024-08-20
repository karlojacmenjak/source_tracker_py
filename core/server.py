from contextlib import asynccontextmanager
from typing import Any, Generator

from fastapi import FastAPI
from uvicorn import Server

from api import router
from core.constant import AppConstants, UvicornConfig
from core.database.local_database import db


@asynccontextmanager
async def on_startup(app: FastAPI) -> Generator[None, Any, None]:  # type: ignore
    await db.setup()

    yield


def init_routers(app: FastAPI) -> None:
    app.include_router(router=router)


def create_app() -> FastAPI:
    _app = FastAPI(
        title=AppConstants.title,
        description=AppConstants.description,
        lifespan=on_startup,
    )
    init_routers(app=_app)
    return _app


app = create_app()


async def run_api() -> None:
    server = Server(config=UvicornConfig(app))
    try:
        await server.serve(sockets=None)
    finally:
        await server.shutdown()

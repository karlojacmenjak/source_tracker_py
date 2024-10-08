from contextlib import asynccontextmanager
from typing import Any, Generator

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from uvicorn import Server

from api import router
from core.constant import AppConstants, UvicornConfig
from core.database.local_database import local_db


@asynccontextmanager
async def on_startup(app: FastAPI) -> Generator[None, Any, None]:  # type: ignore
    await local_db.setup()

    yield


def init_routers(app: FastAPI) -> None:
    app.include_router(router=router)


def init_mount(app: FastAPI) -> None:
    app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")


def create_app() -> FastAPI:
    _app = FastAPI(
        title=AppConstants.title,
        description=AppConstants.description,
        lifespan=on_startup,
    )
    init_routers(app=_app)
    init_mount(app=_app)
    return _app


app = create_app()


@app.exception_handler(404)
async def error_redirect(_, __) -> RedirectResponse:
    return RedirectResponse("/v1/404")


async def run_api() -> None:
    server = Server(config=UvicornConfig(app))
    try:
        await server.serve(sockets=None)
    finally:
        await server.shutdown()

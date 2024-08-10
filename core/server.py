from fastapi import FastAPI

from core.constant import AppConstants


def create_app() -> FastAPI:
    _app = FastAPI(
        title=AppConstants.title,
        description=AppConstants.description,
    )
    return _app


app = create_app()

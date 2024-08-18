from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .v1 import v1_router

router = APIRouter()
router.include_router(v1_router, prefix="/v1")


@router.get("/")
def webpage_redirect() -> RedirectResponse:
    return RedirectResponse("/v1")


__all__ = ["router"]

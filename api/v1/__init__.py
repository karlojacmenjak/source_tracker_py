from fastapi import APIRouter

from .pages import pages_router

v1_router = APIRouter()
v1_router.include_router(pages_router)

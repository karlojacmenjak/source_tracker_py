from fastapi import APIRouter

from .auth import oauth2_router
from .pages import pages_router

v1_router = APIRouter()
v1_router.include_router(pages_router)
v1_router.include_router(oauth2_router)

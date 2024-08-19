from fastapi import APIRouter

oauth2_router = APIRouter()


@oauth2_router.get("/callback")
async def callback(code: str):
    pass

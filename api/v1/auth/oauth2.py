from fastapi import APIRouter

oauth2_router = APIRouter()


@oauth2_router.get("/callback")
async def callback(
    await discord_api.setup()

    data = {
        "client_id": os.environ[DiscordAPI.client_id],
        "client_secret": os.environ[DiscordAPI.client_secret],
        "redirect_uri": DiscordAPI.redirect_uri,
        "grant_type": "authorization_code",
        "code": code,
    }

    result = await discord_api.get_token_response(data)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid Auth Code")

    token, refresh_token, expires_in = result
    print(token, refresh_token, expires_in)
    user = await discord_api.get_user(token)
    user_id = user.get("id")
    await discord_api.close()

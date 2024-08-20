from pydantic import BaseModel


class DiscordUserModel(BaseModel):
    id: str
    username: str
    discriminator: str
    global_name: str | None = None
    avatar: str | None = None
    bot: bool | None = None
    system: bool | None = None
    mfa_enabled: bool | None = None
    banner: str | None = None
    accent_color: str | None = None
    locale: str | None = None
    verified: bool | None = None
    email: str | None = None
    flags: int | None = None
    premium_type: int | None = None
    public_flags: int | None = None

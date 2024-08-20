from pydantic import BaseModel


class OAuth2BodyData(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str
    grant_type: str
    code: str

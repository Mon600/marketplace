from pydantic import BaseModel


class AccessTokenPayload(BaseModel):
    sub: str
    exp: int

class RefreshTokenPayload(AccessTokenPayload):
    jti: str




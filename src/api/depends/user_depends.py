from fastapi import Depends, Request

from typing import Annotated

from api.Bearers.cookie_bearer import CookieBearer
from api.utils.auth import decode_token
from schemas.token_schemas import TokenPayload



cookie_refresh_security = CookieBearer('users_refresh_token')
cookie_access_security = CookieBearer('users_access_token')

async def get_current_user_refresh(

        token: str = Depends(cookie_refresh_security)
) -> TokenPayload:
    payload = decode_token(token)
    return TokenPayload(**payload)


current_user_refresh = Annotated[TokenPayload, Depends(get_current_user_refresh)]

async def get_current_user_access(

    token: str = Depends(cookie_access_security)
) -> TokenPayload:
    payload = decode_token(token)
    return TokenPayload(**payload)

current_user_access = Annotated[TokenPayload, Depends(get_current_user_access)]

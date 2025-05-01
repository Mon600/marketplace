
from fastapi import Depends,  HTTPException

from typing import Annotated, Any

from api.Bearers.cookie_bearer import CookieBearer
from api.depends.redis_depend import RedisDep
from api.depends.repositories_depend import token_repository
from api.depends.service_depend import user_service
from api.utils.auth import decode_token
from schemas.token_schemas import RefreshTokenPayload, AccessTokenPayload

cookie_security = CookieBearer()


async def get_current_user_refresh(
        redis: RedisDep,
        repository: token_repository,
        token: str = Depends(cookie_security)
) -> dict[str, Any]:
    payload = decode_token(token['refresh_token'])
    status_redis = await redis.get(payload["jti"])
    if status_redis is None:
        status_db = await repository.add_token(int(payload["sub"]), payload["jti"])
        if status_db:
            return {"payload": RefreshTokenPayload(**payload), "status": False}
        await redis.set(payload["jti"], int(not status_db), ex=86400 * 30)
    elif not int(status_redis):
        return {"payload": RefreshTokenPayload(**payload), "status": False}
    return {"payload": RefreshTokenPayload(**payload), "status": True}


current_user_refresh = Annotated[RefreshTokenPayload, Depends(get_current_user_refresh)]

async def get_current_user_access(
    refresh_status: current_user_refresh,
    token: str = Depends(cookie_security)
) -> AccessTokenPayload:
    if refresh_status["status"]:
        try:
            payload_access = decode_token(token['access_token'])
            return AccessTokenPayload(**payload_access)
        except KeyError:
            raise HTTPException(status_code=403, detail="access token is invalid")
    raise HTTPException(status_code=401, detail="You've been banned.")

current_user_access = Annotated[AccessTokenPayload, Depends(get_current_user_access)]

async def get_status(user: current_user_access, service: user_service, redis: RedisDep):
    if await redis.get(f"role_{user.sub}") == "admin":
        return True
    role = await service.get_user_role(int(user.sub))
    await redis.set(f"role_{user.sub}", role.role, ex=86400)
    if role.role == 'admin':
        return 'admin'
    elif role.role == 'moderator':
        return 'moderator'
    elif role.role == 'user':
        return HTTPException(status_code=401, detail="Access denied")

StatusDep = Annotated[bool, Depends(get_status)]

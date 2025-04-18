from functools import wraps
from typing import Callable, Coroutine, Any

from fastapi import HTTPException


def is_admin():
    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            service = kwargs.get('u_service')
            user = kwargs.get('user')
            role = await service.get_user_role(int(user.sub))
            if role.role != 'admin':  # Проверяем на admin вместо user
                raise HTTPException(
                    status_code=403,
                    detail="Access denied"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator
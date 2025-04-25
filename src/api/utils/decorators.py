from functools import wraps
from typing import Callable, Coroutine, Any, Annotated

from fastapi import HTTPException, Depends

from api.depends.service_depend import get_user_service, user_service
from api.depends.user_depends import get_current_user_access, get_current_user_refresh, current_user_access


def is_admin(func: Callable[..., Coroutine[Any, Any, Any]]):
    @wraps(func)
    async def wrapper(*args,
                      user: current_user_access ,
                      service: user_service,
                      **kwargs):


        return await func(*args, **kwargs)

    return wrapper



# def is_banned():
#     def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             user = kwargs.get('user')
#             if user is None:
#                 raise HTTPException(status_code=403, detail="You've been banned")
#             return await func(*args, **kwargs)
#         return wrapper
#     return decorator
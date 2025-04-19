from fastapi import APIRouter

from api.depends.service_depend import admin_service, user_service
from api.depends.user_depends import current_user_access
from api.utils.decorators import is_admin

router = APIRouter(tags=['Админ-функционал'], prefix='/admin')


@router.put('/')
@is_admin()
async def ban_user(user_id: int, user: current_user_access, u_service: user_service, a_service: admin_service):
    res = await a_service.ban(user_id)
    if res:
        return {'ok': True, "detail": "User has been banned successfully"}

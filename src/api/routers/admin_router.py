from fastapi import APIRouter, HTTPException

from api.depends.service_depend import admin_service, user_service
from api.depends.user_depends import current_user_access
from api.utils.decorators import is_admin

router = APIRouter(tags=['Админ-функционал'], prefix='/admin')


@router.put('/ban/{user_id}', summary="Блокировка пользователя❌")
@is_admin()
async def ban_user(user_id: int,
                   a_service: admin_service,
                   user: current_user_access,
                   u_service: user_service,
                   ):
    try:
        await a_service.ban(user_id)
        return {"ok": True, "detail": "User has been banned."}
    except:
        raise HTTPException(status_code=500, detail='Something went wrong')

@router.put('/unban/{user_id}', summary='Разблокировка пользователя🔓')
@is_admin()
async def unban_user(user_id: int,
                     a_service: admin_service,
                     user: current_user_access,
                     u_service: user_service):
    try:
        await a_service.unban(user_id)
        return {'ok': True, "detail": "User has been unbanned successfully"}
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.put('deactivate/{announcement_id}/}', summary='Скрытие объявления от пользователей⛔️')
@is_admin()
async def delete_announcement(announcement_id: int,
                              a_service: admin_service,
                              user: current_user_access,
                              u_service: user_service):
    try:
        await a_service.delete_announcement(announcement_id)
        return {"ok": True, "detail": "Announcement has been deleted."}
    except:
        raise HTTPException(status_code=404, detail="Announcement not found")
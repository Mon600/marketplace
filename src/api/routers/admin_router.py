from fastapi import APIRouter, HTTPException

from api.depends.service_depend import admin_service, user_service
from api.depends.user_depends import current_user_access, StatusDep
from api.utils.decorators import is_admin

router = APIRouter(tags=['Админ-функционал🛡🗡'], prefix='/admin')


@router.put('/ban/{user_id}', summary="Блокировка пользователя❌")
async def ban_user(user_id: int,
                   service: admin_service, status: StatusDep):
    if status != 'admin':
        raise HTTPException(status_code=401, detail="Access denied")
    try:
        await service.ban(user_id)
        return {"ok": True, "detail": "User has been banned."}
    except:
        raise HTTPException(status_code=500, detail='Something went wrong')

@router.put('/unban/{user_id}', summary='Разблокировка пользователя🔓')
async def unban_user(user_id: int,
                     service: admin_service,
                     status: StatusDep):
    if status != 'admin':
        raise HTTPException(status_code=401, detail="Access denied")
    try:
        await service.unban(user_id)
        return {'ok': True, "detail": "User has been unbanned successfully"}
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.put('/deactivate/{announcement_id}/', summary='Скрытие объявления от пользователей⛔️')
async def delete_announcement(announcement_id: int,
                              service: admin_service,
                              status: StatusDep):
    try:
        await service.delete_announcement(announcement_id)
        return {"ok": True, "detail": "Announcement has been deleted."}
    except:
        raise HTTPException(status_code=404, detail="Announcement not found")


@router.put('/give-role/{user_id}/{role_id}', summary='Изменить роль пользователя🖍')
async def give_role(user_id: int,
                    role_id: int,
                    service: admin_service,
                    status: StatusDep):
    if status != 'admin':
        raise HTTPException(status_code=401, detail="Access denied")
    try:
        await service.give_role(user_id, role_id)
        return {"ok": True, "detail": f"Role with id {role_id} has been gived to user with id {user_id}."}
    except:
        raise HTTPException(status_code=404, detail="Role not found")


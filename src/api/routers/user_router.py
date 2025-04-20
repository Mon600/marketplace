from fastapi import APIRouter, Depends

from api.depends.user_depends import current_user_access
from api.depends.service_depend import user_service

from schemas.user_schemas import SUser, SChange


router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/", summary="Получить мои данныеℹ️")
async def get_user_info(user: current_user_access, service: user_service) -> SUser | None:
    result = await service.get_user_info(user.sub)
    return result

@router.get("/{yandex_id}", summary="Получить данные пользователя по IDℹ️")
async def get_user_info_by_id(yandex_id: int, user: current_user_access, service: user_service) -> SUser | None:
    result = await service.get_user_info(yandex_id)
    return result


@router.put("/update/", summary="Обновление профиля🔄")
async def update_user_info(new_data: SChange, user: current_user_access, service: user_service):
    if await service.update_user_info(user.sub, new_data):
        return {'ok': True, 'detail': "Data successfully updated"}
    else:
        return {'ok': False, 'detail': "Something went wrong"}

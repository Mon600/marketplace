from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends


from api.depends.service_depend import category_service, user_service
from api.depends.user_depends import current_user_access
from api.utils.decorators import is_admin
from schemas.category_schemas import SCategory

router = APIRouter(tags=['Категории'], prefix='/category')


@router.post('/', summary='Создать категорию➕')
@is_admin()
async def create_category(name: str,
                          u_service: user_service,
                          c_service: category_service,
                          user: current_user_access):

    res = await c_service.create_category(name)
    if res:
        return {'ok': True, 'detail': f'Category {name.title()} created successfully'}

@router.get('/', summary='Список всех категорий📋')
async def get_all_categories(service: category_service) -> list[SCategory]:
    res = await service.get_categories()
    return res

@router.delete('/{id}', summary='Удалить категорию➖')
@is_admin()
async def delete_category(id: int,
                          user: current_user_access,
                          u_service: user_service,
                          service: category_service):
    res = await service.delete_category(id)
    if res:
        return {'ok': True, "detail": f'Category {id} deleted successfully'}
    else:
        return {'ok': False, 'detail': f'Category {id} not found'}


@router.put('/{id}', summary='Изменить категорию🔄')
@is_admin()
async def update_category(data: Annotated[SCategory, Depends()],
                          user: current_user_access,
                          service: category_service,
                          u_service: user_service):
    res = await service.update_category(data)
    if res:
        return {'ok': True, 'detail': f'Category {data.id} updated successfully'}
    else:
        return {'ok': False, 'detail': f'Category {data.id} not found'}


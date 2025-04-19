from fastapi import Depends
from typing import Annotated

from api.depends.redis_depend import RedisDep
from api.depends.repositories_depend import user_repository, announcement_repository, file_repository, \
    category_repository, token_repository
from db.repositories.token_repository import TokenRepository
from services.admin_service import AdminService
from services.announcements_service import AnnouncementService
from services.auth_service import AuthService
from services.category_service import CategoryService
from services.file_service import FileService
from services.user_service import UserService


def get_auth_service(u_repository: user_repository, t_repository: token_repository, redis: RedisDep) -> AuthService:
    return AuthService(u_repository, t_repository, redis)

auth_service = Annotated[AuthService, Depends(get_auth_service)]

def get_user_service(repository: user_repository) -> UserService:
    return UserService(repository)

user_service = Annotated[UserService, Depends(get_user_service)]

def get_announcement_service(repository: announcement_repository) -> AnnouncementService:
    return AnnouncementService(repository)

announcement_service = Annotated[AnnouncementService, Depends(get_announcement_service)]


def get_file_service(repository: file_repository) -> FileService:
    return FileService(repository)

file_service = Annotated[FileService, Depends(get_file_service)]

def get_category_service(repository: category_repository) -> CategoryService:
    return CategoryService(repository)

category_service = Annotated[CategoryService, Depends(get_category_service)]

def get_admin_service(u_rep: user_repository,
                      redis: RedisDep) -> AdminService:
    return AdminService(u_rep, redis)

admin_service = Annotated[AdminService, Depends(get_admin_service)]
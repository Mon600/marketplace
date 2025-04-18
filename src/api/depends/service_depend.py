from fastapi import Depends
from typing import Annotated

from api.depends.repositories_depend import user_repository, announcement_repository, file_repository, \
    category_repository
from services.announcements_service import AnnouncementService
from services.auth_service import AuthService
from services.category_service import CategoryService
from services.file_service import FileService
from services.user_service import UserService


def get_auth_service(repository: user_repository) -> AuthService:
    return AuthService(repository)

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
import os
import shutil

import aiofiles
from fastapi import UploadFile

from db.repositories.file_repository import FileRepository
from schemas.file_schemas import SFile


class FileService:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    @staticmethod
    async def files_to_dirs(user_id: int, announcement_id, files: list[UploadFile], number = 1) -> list[SFile]:
        dir = f'../files/{user_id}/{announcement_id}'
        dirs = []
        for file in files:
            header = file.headers['content-type']
            if not "image" in str(header):
                raise ValueError("Incorrect file type")
            extension = file.filename.split('.')[-1]
            filename = f"/{number}.{extension}"
            file_dir = dir + filename
            if not os.path.exists(dir):
                os.makedirs(dir, exist_ok=True)
            async with aiofiles.open(file_dir, "wb") as f:
                await f.write(await file.read())
            exemplar = {
                "url": file_dir,
                "type": header,
                "announcement_id": announcement_id
                }
            dirs.append(SFile.model_validate(exemplar))
            number += 1
        return dirs

    @staticmethod
    async def delete_dir(announcement_id: int, user_id: int) -> None:
        dir  = f"../files/{user_id}/{announcement_id}"
        if os.path.exists(dir):
            shutil.rmtree(dir)

    async def add_files(self, files: list[UploadFile], announcement_id: int, user_id) -> None:
        try:
             files = await self.files_to_dirs(user_id, announcement_id, files)
             await self.repository.add_file(files)
        except Exception as e:
            raise e

    async def update_files(self, dirs: list[UploadFile], announcement_id: int, user_id) -> None:
        try:
            files = await self.files_to_dirs(user_id, announcement_id, dirs)
            await self.repository.update_files(files, announcement_id)
        except Exception as e:
            print(e)

    async def delete_files(self, announcement_id: int, user_id) -> None:

        await self.delete_dir(announcement_id, user_id)




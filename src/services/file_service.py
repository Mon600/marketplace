import os

import aiofiles
from fastapi import UploadFile

from db.repositories.announcemets_repository import AnnouncementRepository


class FileService:
    def __init__(self, repository: AnnouncementRepository):
        self.repository = repository

    async def files_to_dirs(self, user_id: int, announcement_id, files: list[UploadFile], number = 1) -> dict | None:
        dir = f'../files/{user_id}/{announcement_id}'
        dirs = {}
        available_names = await self.get_names(user_id, announcement_id)
        if (len(available_names) == 0) or (len(files) > len(available_names)):
            files = files[0:len(available_names) - 1]
        for file in files:
            header = file.headers['content-type']
            if not "image" in str(header):
                raise ValueError("Incorrect file type")
            extension = file.filename.split('.')[-1]
            filename = f"{available_names[0]}.{extension}"
            del available_names[0]
            file_dir = os.path.join(dir, filename)
            dir_name = os.path.dirname(file_dir)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
            dirs[f'image_{number}'] = dir
            async with aiofiles.open(file_dir, "wb") as f:
                await f.write(await file.read())
            number += 1
        return dirs

    @staticmethod
    async def check_len_files(user_id: int, announcement_id: int):
        dir =  f'../files/{user_id}/{announcement_id}'
        return os.listdir(dir)


    async def get_names(self, user_id: int, announcement_id: int):
        all_names = [i for i in range(1, 11)]
        current_list = await self.check_len_files(user_id, announcement_id)
        names = list(map(lambda x: int(x.split('.')[0]), current_list))
        unique_elements = set(names).symmetric_difference(all_names)
        return list(unique_elements)


    async def delete_dirs(self, user_id: int, announcement_id: int, dirs: list[int]) -> None:
        current_list = await self.check_len_files(user_id, announcement_id)
        a = list(map(lambda x: x.split('.'), current_list))
        dirs_dict = {}
        dir = f'../files/{user_id}/{announcement_id}'
        for i in a:
            dirs_dict[int(i[0])] = i[1]
        for i in dirs:
            try:
                file_dir = dir + f'/{i}.{dirs_dict[i]}'
                os.remove(file_dir)
            except:
                continue

    async def save_uploaded_files(self, files: list[UploadFile],user_id: int, announcement_id: int, ):
        try:
            dirs = await self.files_to_dirs(user_id, announcement_id, files)
            dirs['announcement_id'] = announcement_id
        except ValueError as e:
            raise e
        res = await self.repository.update_files(dirs, user_id, announcement_id)
        if res:
            return True
        else:
            return False

    async def update_files(self, files: list[UploadFile], announcement_id: int, user_id: int):
        num = len(await self.check_len_files(user_id, announcement_id))
        max_files = 10
        sum_len = num + len(files)
        if sum_len > max_files:
            num = max_files - (sum_len - max_files)
        dirs = await self.files_to_dirs(user_id, announcement_id, files, number=num + 1)
        res = await self.repository.update_files(dirs,  announcement_id, user_id)
        if res:
            return True
        else:
            return False

    async def delete_files(self, files: list[int], announcement_id: int, user_id: int):
        files_name = list(map(lambda x: f'image_{x}', files))
        files_dict = dict.fromkeys(files_name, '')
        res = await self.repository.delete_files(announcement_id, user_id, files_dict)
        if res:
            await self.delete_dirs(user_id, announcement_id, files)
            return True


from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.models import FileModel as Model, FileModel
from schemas.file_schemas import SFile


class FileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_file(self, files: list[SFile]):
        for file in files:
            new_file = FileModel(**file.model_dump())
            self.session.add(new_file)
        await self.session.commit()
        return True

    async def update_files(self, files: list[SFile], announcement_id: int):

        query = delete(Model).where(Model.announcement_id == announcement_id)
        await self.session.execute(query)
        for file in files:
            new_file = FileModel(**file.model_dump())
            self.session.add(new_file)
        await self.session.commit()
        return True

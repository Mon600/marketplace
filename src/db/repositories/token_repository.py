import datetime

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from db.models.models import TokenModel


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_token(self, user_id, token_id):
        query = (insert(TokenModel)
                 .values(token_id=token_id, user_id=user_id)
                 .on_conflict_do_nothing()
                 .returning(TokenModel.is_banned))
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalars().one()

    async def delete(self, token_id):
        query = delete(TokenModel).where(TokenModel.token_id == token_id)
        await self.session.execute(query)
        await self.session.commit()
        return True

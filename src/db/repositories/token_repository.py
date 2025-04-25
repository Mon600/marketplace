
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


from db.models.models import TokenModel, UserModel


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_token(self, user_id, token_id):
        user_query = select(UserModel.is_active).where(UserModel.yandex_id == user_id)
        user_status = await self.session.execute(user_query)
        is_banned = not user_status.scalars().first()
        query = (insert(TokenModel)
                 .values(token_id=token_id, user_id=user_id, is_banned=is_banned)
                 .on_conflict_do_update(
                        index_elements=[TokenModel.token_id],
                        set_={"is_banned": is_banned}
        )
                 .returning(TokenModel.is_banned))
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalars().one_or_none()

    async def delete(self, token_id):
        query = delete(TokenModel).where(TokenModel.token_id == token_id)
        await self.session.execute(query)
        await self.session.commit()
        return True

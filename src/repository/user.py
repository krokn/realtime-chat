from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.connection import get_async_session
from src.database.models import UserModel


class UserRepository:
    def __init__(self, user_model: UserModel):
        self.obj = user_model

    async def add(self):
        async with get_async_session() as session:
            session.add(self.obj)
            await session.flush()
            user_id = self.obj.id
            await session.commit()
            return user_id

    async def get(self, username: str):
        async with get_async_session() as session:
            query = select(UserModel).where(UserModel.username == username)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    def get_for_celery(username: str, session):
        query = select(UserModel).where(UserModel.username == username)
        result = session.execute(query)
        return result.scalar_one_or_none()

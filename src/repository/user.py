from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.connection import get_async_session
from src.database.models import UserModel


class UserRepository:
    def __init__(self):
        self.model = UserModel

    @staticmethod
    async def add(user: UserModel):
        async with get_async_session() as session:
            session.add(user)
            await session.flush()
            user_id = user
            await session.commit()
            return user_id

    async def get(self, username: str):
        async with get_async_session() as session:
            query = select(self.model).where(self.model.username == username)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    def get_for_celery(username: str, session):
        query = select(UserModel).where(UserModel.username == username)
        result = session.execute(query)
        return result.scalar_one_or_none()

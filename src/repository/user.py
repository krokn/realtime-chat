from sqlalchemy import select

from src.database.connection import get_async_session
from src.database.models import UserModel


class UserRepository:

    @staticmethod
    async def add(user: UserModel):
        async with get_async_session() as session:
            session.add(user)
            await session.flush()
            user_id = user.id
            await session.commit()
            return user_id

    @staticmethod
    async def get(username: str):
        async with get_async_session() as session:
            query = select(UserModel).where(UserModel.username == username)
            result = await session.execute(query)
            return result.scalar_one_or_none()

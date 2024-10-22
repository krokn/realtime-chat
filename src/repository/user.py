from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.database.connection import get_async_session
from src.database.models import UserModel


class UserRepository:
    def __init__(self):
        self.model = UserModel

    @staticmethod
    async def add(user: UserModel):
        try:
            async with get_async_session() as session:
                session.add(user)
                await session.flush()  # Здесь данные фиксируются в сессии
                user_id = user
                await session.commit()  # Подтверждаем изменения в базе данных
                return user_id
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении пользователя: {e}")
            await session.rollback()  # Откатить изменения в случае ошибки
            raise e

    async def get(self, username: str):
        try:
            async with get_async_session() as session:
                query = select(self.model).where(self.model.username == username)
                result = await session.execute(query)
                return result.scalar_one_or_none()  # Вернуть одного пользователя или None, если не найден
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении пользователя с именем '{username}': {e}")
            raise e

    @staticmethod
    def get_for_celery(username: str, session):
        try:
            query = select(UserModel).where(UserModel.username == username)
            result = session.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении пользователя для Celery с именем '{username}': {e}")
            raise e

from loguru import logger
from sqlalchemy import select, and_, or_
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.database.connection import get_async_session
from src.database.models import MessageModel


class MessageRepository:

    def __init__(self):
        self.repository = MessageModel

    @staticmethod
    def add(message: MessageModel, session):
        try:
            session.add(message)
            session.flush()  # Фиксируем изменения в сессии
            session.commit()  # Подтверждаем изменения в базе данных
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении сообщения: {e}")
            session.rollback()  # Откатить изменения в случае ошибки
            raise e

    async def get_all(self, first_user_id, second_user_id):
        try:
            async with get_async_session() as session:
                query = select(self.repository).where(and_(
                    or_(self.repository.sender_id == first_user_id, self.repository.sender_id == second_user_id),
                    or_(self.repository.receiver_id == first_user_id, self.repository.receiver_id == second_user_id)
                ))
                result = await session.execute(query)
                return result.scalars().all()  # Возвращаем список всех сообщений
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении сообщений между пользователями с ID {first_user_id} и {second_user_id}: {e}")
            raise e

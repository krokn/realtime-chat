from sqlalchemy import select, and_, or_

from src.database.connection import get_async_session
from src.database.models import MessageModel


class MessageRepository:

    def __init__(self):
        self.repository = MessageModel

    @staticmethod
    def add(message: MessageModel, session):
        session.add(message)
        session.flush()
        session.commit()

    async def get_all(self, first_user_id, second_user_id):
        async with get_async_session() as session:
            query = select(self.repository).where(and_(
                or_(self.repository.sender_id == first_user_id, self.repository.sender_id == second_user_id),
                or_(self.repository.receiver_id == first_user_id, self.repository.receiver_id == second_user_id)
            ))
            result = await session.execute(query)
            return result.scalars().all()



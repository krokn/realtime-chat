from sqlalchemy import select

from src.database.models import MessageModel


class MessageRepository:

    def __init__(self, message_model: MessageModel):
        self.obj = message_model
        self.repository = MessageModel

    def add(self, session):
        session.add(self.obj)
        session.flush()
        session.commit()

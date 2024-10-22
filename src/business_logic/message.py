from src.database.models import MessageModel


class Message:

    @staticmethod
    def create_message_model(sender_id, receiver_id, message):
        message_model = MessageModel(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=message
        )
        return message_model

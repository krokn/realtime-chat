from loguru import logger
from starlette.websockets import WebSocket

from src.services.celery import send_notification_celery, save_message
from src.services.redis import redis_client


class WebSocketManager:
    def __init__(self):
        self.redis_prefix = "active_user:"
        self.active_connections: dict[str, WebSocket] = {}  # Храним активные соединения WebSocket

    async def connect(self, websocket: WebSocket, sender: str):
        await websocket.accept()
        self.active_connections[sender] = websocket  # Храним соединение WebSocket
        await redis_client.set(f"{self.redis_prefix}{sender}", "connected")
        logger.info(f'Пользователь {sender} подключен.')
        logger.info(f"Активные соединения: {self.active_connections.keys()}")

    async def disconnect(self, sender: str):
        await redis_client.delete(f"{self.redis_prefix}{sender}")
        if sender in self.active_connections:
            del self.active_connections[sender]  # Удаляем соединение WebSocket
        logger.info(f'Пользователь {sender} отключен.')
        logger.info(f"Активные соединения: {self.active_connections.keys()}")

    async def send_message_user(self, recipient: str, message: str, sender: str):
        # Проверяем, существует ли получатель в активных соединениях
        recipient_ws = self.active_connections.get(recipient)
        logger.info(f"Сообщение от {sender} к {recipient}: {message}")
        save_message.delay(sender, recipient, message)
        logger.info(f"Активные соединения: {self.active_connections.keys()}")
        if recipient_ws:
            logger.info(f'{recipient} is online')
            await recipient_ws.send_text(f"{sender}: {message}")  # Отправляем сообщение получателю в реальном времени
        else:
            logger.info(f'{recipient} is offline')
            send_notification_celery.delay(recipient, f'{sender}: {message}') # Отправляем уведомление в телеграм


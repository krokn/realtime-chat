from loguru import logger
from starlette.websockets import WebSocket

from src.services.celery import send_notification_celery, save_message
from src.services.redis import redis_client


class WebSocketManager:
    def __init__(self):
        self.redis_prefix = "active_user:"
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, sender: str):
        await websocket.accept()
        self.active_connections[sender] = websocket
        # Сохраняем информацию о подключении в Redis
        await redis_client.set(f"{self.redis_prefix}{sender}", "connected")
        logger.info(f'Пользователь {sender} подключен.')
        logger.info(f"Активные соединения после подключения {sender}: {list(self.active_connections.keys())}")

    async def disconnect(self, sender: str):
        # Удаляем информацию о пользователе из Redis
        await redis_client.delete(f"{self.redis_prefix}{sender}")
        if sender in self.active_connections:
            del self.active_connections[sender]
        logger.info(f'Пользователь {sender} отключен.')
        logger.info(f"Активные соединения после отключения {sender}: {list(self.active_connections.keys())}")

    async def is_user_online(self, recipient: str) -> bool:
        """Проверка в Redis, подключен ли пользователь"""
        return await redis_client.exists(f"{self.redis_prefix}{recipient}")

    async def send_message_user(self, recipient: str, message: str, sender: str):
        recipient_ws = self.active_connections.get(recipient)
        logger.info(f"Сообщение от {sender} к {recipient}: {message}")
        save_message.delay(sender, recipient, message)

        # Проверяем наличие активного соединения через Redis
        is_online = await self.is_user_online(recipient)
        logger.info(f"Активные соединения: {list(self.active_connections.keys())}")

        if is_online and recipient_ws:
            logger.info(f'{recipient} is online')
            await recipient_ws.send_text(f"{sender}: {message}")
        else:
            logger.info(f'{recipient} is offline, отправляем уведомление через Telegram')
            send_notification_celery.delay(recipient, f'{sender}: {message}')
from loguru import logger
from starlette.websockets import WebSocket

from src.services.celery import send_notification_celery, save_message
from src.services.redis import redis_client


class WebSocketManager:
    def __init__(self):
        self.redis_prefix = "active_user:"
        self.active_connections: dict[str, WebSocket] = {}  # Храним активные соединения WebSocket

    async def connect(self, websocket: WebSocket, sender: str):
        # Если уже есть подключение для этого пользователя, отключаем его
        if sender in self.active_connections:
            logger.warning(f"Пользователь {sender} уже подключен. Переподключение...")
            await self.disconnect(sender)

        await websocket.accept()
        self.active_connections[sender] = websocket  # Сохраняем новое подключение
        await redis_client.set(f"{self.redis_prefix}{sender}", "connected")
        logger.info(f'Пользователь {sender} подключен.')
        logger.info(f"Активные соединения после подключения {sender}: {list(self.active_connections.keys())}")

    async def disconnect(self, sender: str):
        # Проверяем, есть ли это соединение перед удалением
        if sender in self.active_connections:
            await self.active_connections[sender].close()  # Закрываем WebSocket
            del self.active_connections[sender]  # Удаляем соединение из активных
            await redis_client.delete(f"{self.redis_prefix}{sender}")
            logger.info(f'Пользователь {sender} отключен.')
        else:
            logger.warning(f'Попытка отключить {sender}, но его нет среди активных соединений.')

        logger.info(f"Активные соединения после отключения {sender}: {list(self.active_connections.keys())}")

    async def send_message_user(self, recipient: str, message: str, sender: str):
        # Проверяем наличие соединения с получателем
        recipient_ws = self.active_connections.get(recipient)
        logger.info(f"Сообщение от {sender} к {recipient}: {message}")

        # Сохраняем сообщение через Celery
        save_message.delay(sender, recipient, message)

        if recipient_ws:
            logger.info(f'{recipient} is online')
            try:
                await recipient_ws.send_text(f"{sender}: {message}")  # Отправляем сообщение получателю
            except Exception as e:
                logger.error(f"Ошибка отправки сообщения пользователю {recipient}: {e}")
        else:
            logger.info(f'{recipient} is offline, отправляем уведомление через Telegram')
            send_notification_celery.delay(recipient, f'{sender}: {message}')

        logger.info(f"Активные соединения после отправки сообщения: {list(self.active_connections.keys())}")
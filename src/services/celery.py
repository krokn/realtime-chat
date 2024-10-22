import asyncio
from celery import Celery
from loguru import logger

from src.database.connection import get_sync_session
from src.repository.user import UserRepository
from src.services.telegram_bot import send_notification

celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@celery.task
def send_notification_celery(username: str, text: str):
    user = UserRepository.get_for_celery(username, get_sync_session())

    if user:
        try:
            loop = asyncio.get_event_loop()
            
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            loop.run_until_complete(send_notification(user.telegram_id, text))

        except RuntimeError as e:
            logger.error(f"Ошибка выполнения event loop: {e}")
        except Exception as e:
            logger.error(f"Не удалось отправить уведомление: {e}")
    else:
        logger.warning(f"User {username} not found.")

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

from loguru import logger

BOT_TOKEN = '7756693894:AAFB0mLHh9vJOaem9XnAI8yOQkzR-zYuLj0'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    telegram_id = message.from_user.id
    await message.answer(f"Ваш Telegram ID: {telegram_id}")

async def send_notification(user_id: int, text: str):
    try:
        await bot.send_message(chat_id=user_id, text=text)
        logger.info(f"Уведомление отправлено пользователю {user_id}: '{text}'")
    except Exception as e:
        logger.error(f"Не удалось отправить уведомление пользователю {user_id}: {e}")



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

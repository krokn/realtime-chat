from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

BOT_TOKEN = '7756693894:AAFB0mLHh9vJOaem9XnAI8yOQkzR-zYuLj0'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    telegram_id = message.from_user.id
    await message.answer(f"Ваш Telegram ID: {telegram_id}")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

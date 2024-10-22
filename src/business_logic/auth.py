from fastapi import HTTPException
from loguru import logger

from config import SECONDS_PER_SAVE_IN_REDIS
from src.database.models import UserModel
from src.repository.user import UserRepository
from src.services.encryption import Encryption
from src.services.redis import redis_client


class AuthService:
    @staticmethod
    async def register(user_data):
        logger.info(f'username = {user_data.username}, password = {user_data.password}')

        # Хеширование пароля
        hash_password = Encryption.hash(user_data.password)
        user_model = UserModel(
            username=user_data.username,
            password=hash_password,
            telegram_id=user_data.telegram_id
        )

        # Добавление пользователя в базу данных
        await UserRepository().add(user_model)
        return 'success'

    @staticmethod
    async def login(user_data):
        logger.info(f'username = {user_data.username}, password = {user_data.password}')

        # Получение пользователя из базы данных
        user_db = await UserRepository().get(user_data.username)

        if user_db is None:
            raise HTTPException(status_code=404, detail="user not found")

        # Проверка пароля
        if Encryption.hash(user_data.password) != user_db.password:
            raise HTTPException(status_code=405, detail="password incorrect")

        # Генерация токена
        token = Encryption.create_token(user_db.username)

        # Сохранение токена в Redis
        await redis_client.set(token, user_db.username, ex=SECONDS_PER_SAVE_IN_REDIS)
        logger.info(f'token = {token}')

        return {'token': token}
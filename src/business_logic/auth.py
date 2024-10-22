from fastapi import HTTPException
from loguru import logger

from src.business_logic.user import User
from src.database.models import UserModel
from src.repository.user import UserRepository
from src.schemas.user import UserSchemaForAdd
from src.services.encryption import Encryption
from src.services.redis import redis_client

SECONDS_PER_SAVE_IN_REDIS = 120 * 60



class AuthService:
    @staticmethod
    async def register(user_data):
        hash_password = Encryption.hash(user_data.password)
        user_model = await User().create_user_model(UserSchemaForAdd, hash_password)
        repository = UserRepository()
        await repository.add(user_model)
        return 'user registered success'

    @staticmethod
    async def login(user_data):
        logger.info(f'username = {user_data.username}, password = {user_data.password}')
        repository = UserRepository()
        user_db = await repository.get(user_data.username)

        if user_db is None:
            raise HTTPException(status_code=404, detail="user not found")

        if Encryption.hash(user_data.password) != user_db.password:
            raise HTTPException(status_code=405, detail="password incorrect")

        token = Encryption.create_token(user_db.username)

        await redis_client.set(token, user_db.username, ex=SECONDS_PER_SAVE_IN_REDIS)
        logger.info(f'token = {token}')

        return {'token': token}

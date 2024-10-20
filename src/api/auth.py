from fastapi import APIRouter, HTTPException
from loguru import logger

from src.database.models import UserModel
from src.repository.user import UserRepository
from src.schemas.user import UserSchemaForAdd
from src.services.encryption import Encryption
from src.services.redis import RedisClient, redis_client

router = APIRouter(
    prefix='/api/auth',
    tags=['Auth']
)


@router.post('/register')
async def register(user: UserSchemaForAdd):
    logger.info(f'username = {user.username}, password = {user.password}')
    hash_password = Encryption.hash(user.password)
    user_model = UserModel(
        username=user.username,
        password=hash_password
    )
    await UserRepository().add(user_model)
    return 'success'


@router.post('/login')
async def login(user: UserSchemaForAdd):
    logger.info(f'username = {user.username}, password = {user.password}')
    user_db = await UserRepository().get(user.username)
    if user_db is None:
        raise HTTPException(status_code=404, detail="user not found")

    if Encryption.hash(user.password) != user_db.password:
        raise HTTPException(status_code=405, detail="password incorrect")
    token = Encryption.create_token(user_db.id)
    await redis_client.set(token, user_db.id, ex=120 * 60)
    logger.info(f'token = {token}')
    response = {
        'token': token
    }
    return response






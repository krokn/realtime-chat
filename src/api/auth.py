from fastapi import APIRouter, HTTPException
from loguru import logger

from src.business_logic.auth import AuthService
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
    return await AuthService.register(user)


@router.post('/login')
async def login(user: UserSchemaForAdd):
    return await AuthService.login(user)






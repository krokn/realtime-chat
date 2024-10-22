from fastapi import APIRouter, HTTPException
from loguru import logger

from src.business_logic.auth import AuthService
from src.database.models import UserModel
from src.repository.user import UserRepository
from src.schemas.user import UserSchemaForAdd, UserSchemaForLogin
from src.services.encryption import Encryption
from src.services.redis import RedisClient, redis_client

router = APIRouter(
    prefix='/api/auth',
    tags=['Auth']
)


@router.post(
    '/register',
    summary="Регистрация нового пользователя",
    description=(
        "Этот endpoint позволяет зарегистрировать нового пользователя, предоставив "
        "имя пользователя, пароль и Telegram ID. После успешной регистрации, "
        "пользователь будет добавлен в базу данных."
    ),
    response_description="Успешная регистрация пользователя"
)
async def register(user: UserSchemaForAdd):
    return await AuthService.register(user)


@router.post(
    '/login',
    summary="Авторизация пользователя",
    description=(
        "Этот endpoint выполняет авторизацию пользователя по предоставленным имени пользователя и паролю. "
        "После успешной авторизации возвращает токен, который можно использовать для доступа к чату."
    ),
    response_description="Успешная авторизация и возврат токена",
    responses={
        200: {
            "description": "Успешная авторизация",
            "content": {
                "application/json": {
                    "example": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
                }
            },
        },
        404: {
            "description": "Пользователь не найден",
            "content": {
                "application/json": {
                    "example": {"detail": "user not found"}
                }
            },
        },
        405: {
            "description": "Неверный пароль",
            "content": {
                "application/json": {
                    "example": {"detail": "password incorrect"}
                }
            },
        },
    }
)
async def login(user: UserSchemaForLogin):
    return await AuthService.login(user)






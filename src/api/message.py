from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger
from starlette.responses import JSONResponse

from src.repository.message import MessageRepository
from src.repository.user import UserRepository
from src.services.redis import redis_client
from src.business_logic.websocket_manager import WebSocketManager

router = APIRouter(
    prefix='/api/message',
    tags=['Message']
)


ws_manager = WebSocketManager()


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket, token: str):
    user = await redis_client.get(token)
    if not user:
        await websocket.close(code=1008)
        return

    sender = user.decode("utf-8")
    await ws_manager.connect(websocket, sender)
    try:
        while True:
            data = await websocket.receive_text()
            recipient, message = data.split("|", 1)  # Разделяем сообщение на получателя и текст
            recipient = recipient.strip()
            await ws_manager.send_message_user(recipient, message, sender)
    except WebSocketDisconnect:
        await ws_manager.disconnect(sender)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await ws_manager.disconnect(sender)


@router.get(
    "/ws-info",
    summary="Информация о WebSocket подключении для обмена сообщениями",
    description=(
        "Этот WebSocket эндпоинт (`/ws`) позволяет пользователям отправлять сообщения друг другу в реальном времени. "
        "Соединение открывается с помощью токена авторизации, который должен быть передан как параметр. После подключения "
        "пользователь может отправлять сообщения в формате `получатель|сообщение`, и сервер отправит сообщение указанному "
        "пользователю, если он подключен."
    ),
    response_description="Информация о WebSocket соединении",
    tags=["WebSocket"]
)
async def ws_info():
    return JSONResponse(content={
        "detail": "WebSocket соединение осуществляется по адресу `/ws`.",
        "connection": "Передайте токен авторизации в качестве параметра в WebSocket соединении.",
        "usage": "После подключения отправляйте сообщения в формате `получатель|сообщение`."
    })


@router.get(
    '/correspondence',
    summary="Получение переписки между пользователями",
    description=(
        "Этот endpoint позволяет получить всю историю переписки между двумя пользователями, "
        "указанными по их именам пользователя. История сообщений возвращается в формате списка объектов."
    ),
    response_description="История переписки в формате JSON",
    responses={
        200: {
            "description": "Успешное получение переписки",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "sender_id": 123,
                            "receiver_id": 456,
                            "message": "Привет!",
                            "timestamp": "2024-10-22T10:00:00Z"
                        },
                        {
                            "id": 2,
                            "sender_id": 456,
                            "receiver_id": 123,
                            "message": "Привет, как дела?",
                            "timestamp": "2024-10-22T10:05:00Z"
                        }
                    ]
                }
            },
        },
        404: {
            "description": "Один из пользователей не найден",
            "content": {
                "application/json": {
                    "example": {"detail": "user not found"}
                }
            },
        },
    },
    tags=["Переписка"]
)
async def get_correspondence(first_username: str, second_username: str):
    first_user = await UserRepository().get(first_username)
    second_user = await UserRepository().get(second_username)
    messages = await MessageRepository().get_all(first_user.id, second_user.id)
    messages_dict = [message.to_dict() for message in messages]
    return JSONResponse(status_code=200, content=messages_dict)
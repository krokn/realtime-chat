from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger
from starlette.responses import JSONResponse

from src.business_logic.message import Message
from src.repository.message import MessageRepository
from src.repository.user import UserRepository
from src.services.redis import redis_client
from src.services.websocket_manager import WebSocketManager

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


@router.get('/correspondence')
async def get_correspondence(first_username: str, second_username):
    first_user = await UserRepository().get(first_username)
    second_user = await UserRepository().get(second_username)
    messages = await MessageRepository().get_all(first_user.id, second_user.id)
    messages_dict = [message.to_dict() for message in messages]
    return JSONResponse(status_code=200, content=messages_dict)
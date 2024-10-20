from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger

from src.services.redis import redis_client
from src.services.websocket_manager import WebSocketManager

router = APIRouter(
    prefix='/api/message',
    tags=['Message']
)

ws_manager = WebSocketManager()


@router.websocket("/ws")
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
            message, recipient = await ws_manager.parse_data(data)
            await ws_manager.send_message(recipient, message, sender)
    except WebSocketDisconnect:
        ws_manager.disconnect(sender)
    except Exception as e:
        logger.error(f"Error: {e}")
        ws_manager.disconnect(sender)

from loguru import logger
from starlette.websockets import WebSocket


class WebSocketManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, sender: str, recipient: str, message: str):
        if recipient in self.active_connections:
            recipient_ws = self.active_connections[recipient]
            await recipient_ws.send_text(f"{sender}: {message}")
        else:
            pass
        return True

    @staticmethod
    async def parse_data(data):
        parsed_data = data.split("|", 1)
        recipient_id = parsed_data[0]
        message_content = parsed_data[1] if len(parsed_data) > 1 else ""
        return message_content, recipient_id

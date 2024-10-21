from loguru import logger
from starlette.websockets import WebSocket


class WebSocketManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, sender: str):
        await websocket.accept()
        self.active_connections[sender] = websocket
        logger.info(f'User {sender} connected.')

    def disconnect(self, sender: str):
        if sender in self.active_connections:
            del self.active_connections[sender]
        logger.info(f'User {sender} disconnected.')

    async def send_message_user(self, recipient: str, message: str, sender: str):
        if recipient in self.active_connections:
            recipient_ws = self.active_connections[recipient]
            await recipient_ws.send_text(f"{sender}: {message}")
        else:
            logger.warning(f"User {recipient} not connected.")
        return True

    @staticmethod
    async def parse_data(data):
        parsed_data = data.split("|", 1)
        recipient = parsed_data[0]
        message = parsed_data[1] if len(parsed_data) > 1 else ""
        logger.info(f'message = {message}, recipient = {recipient}')
        return message, recipient

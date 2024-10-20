from src.api.auth import router as auth_router
from src.api.message import router as message_router

all_routers = [
    auth_router,
    message_router
]
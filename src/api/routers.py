from src.api.auth import router as auth_router
from src.api.message import router as message_router
from src.api.user import router as user_router

all_routers = [
    auth_router,
    message_router,
    user_router
]
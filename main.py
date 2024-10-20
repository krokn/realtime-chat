from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.routers import all_routers

app = FastAPI(
    title="Сервис обмена сообщениями"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router)

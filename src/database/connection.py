from contextlib import asynccontextmanager
from typing import AsyncGenerator

from requests import session
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


class Base(DeclarativeBase):
    pass

SYNC_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(ASYNC_DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine)

engine = create_engine(SYNC_DATABASE_URL)
SyncSession = sessionmaker(bind=engine)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_sync_session():
    return SyncSession()
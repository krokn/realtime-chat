import redis.asyncio as aioredis


class RedisClient:
    def __init__(self):
        self.redis = aioredis.from_url("redis://redis:6379")

    async def set(self, key: str, value: str, ex: int):
        await self.redis.set(key, value, ex=ex)

    async def get(self, key: str):
        return await self.redis.get(key)


redis_client = RedisClient()

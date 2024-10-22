import redis.asyncio as aioredis


class RedisClient:
    def __init__(self):
        self.redis = aioredis.from_url("redis://redis:6379")

    async def set(self, key: str, value: str, ex: int = None):
        await self.redis.set(key, value, ex=ex)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def get_all_keys(self, pattern: str):
        return await self.redis.keys(pattern)

redis_client = RedisClient()

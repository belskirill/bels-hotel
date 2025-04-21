import logging

import redis.asyncio as redis


class RedisManager:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        logging.info("Начинаю подключение к Redis...")
        self.redis = await redis.Redis(host=self.host, port=self.port)
        logging.info("Успешное подключение к Redis...")

    async def set(self, key, value, expire):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key):
        return await self.redis.get(key)

    async def delete(self, key):
        await self.redis.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.close()

from redis.asyncio import Redis, from_url

from app.core.config import config


class RedisManager:
    def __init__(self):
        self.redis: Redis = from_url(
            config.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    
    async def cashe_avatar(self, card_id: int, url: str) -> None:
        await self.redis.set(f"avatar:{card_id}", url, ex=config.IMAGE_EXPIRE_TIME)

    async def get_cashed_avatar(self, card_id: int) -> str | None:
        return await self.redis.get(f"avatar:{card_id}")

    async def close(self) -> None:
        await self.redis.close()

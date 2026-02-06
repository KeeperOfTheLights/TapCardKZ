from fastapi import FastAPI
from app.core.redis import RedisManager
from app.core.logger import logger


async def set_up(app: FastAPI) -> None:
    logger.info("Initializing Redis manager...")
    app.state.redis_manager = RedisManager()
    logger.info("Redis manager initialized")


async def clean_up(app: FastAPI) -> None:
    logger.info("Closing Redis connection...")
    redis_manager: RedisManager = getattr(app.state, "redis_manager", None)
    if redis_manager:
        await redis_manager.close()
    logger.info("Redis connection closed")

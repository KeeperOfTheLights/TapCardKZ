from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.app_state import db, s3, redis
from app.core.config import config
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logger.info("App starting...")
    await db.set_up(app)
    await redis.set_up(app)
    s3.set_up(app)
    yield
    # shutdown
    logger.info("App shutting down...")
    await db.clean_up(app)
    await redis.clean_up(app)
    s3.clean_up(app)
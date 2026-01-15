from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.app_state import setup_db, cleanup_db, setup_s3, cleanup_s3
from app.core.config import config
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logger.info("App starting...")
    await setup_db(app)
    await setup_s3(app)
    yield
    # shutdown
    logger.info("App shutting down...")
    await cleanup_db(app)
    await cleanup_s3(app)
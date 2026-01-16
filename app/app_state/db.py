from fastapi import FastAPI
from app.core.manager import AsyncDatabaseManager
from app.core.logger import logger


async def set_up(app: FastAPI) -> None:
    logger.info("Initializing database manager...")
    app.state.db_manager = AsyncDatabaseManager()
    logger.info("Database manager initialized")
    await app.state.db_manager.create_all_tables()


async def clean_up(app: FastAPI) -> None:
    logger.info("Disposing database engine...")
    db_manager: AsyncDatabaseManager = getattr(app.state, "db_manager", None)
    if db_manager:
        await db_manager.dispose()
    logger.info("Database engine disposed")
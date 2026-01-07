from fastapi import FastAPI
from app.core.manager import AsyncDatabaseManager


async def setup_db(app: FastAPI) -> None:
    """Initialize database manager and attach to app state"""
    print("Initializing database manager...")
    app.state.db_manager = AsyncDatabaseManager()
    print("Database manager initialized")
    await app.state.db_manager.create_all_tables()


async def cleanup_db(app: FastAPI) -> None:
    """Cleanup database connections"""
    print("Disposing database engine...")
    db_manager: AsyncDatabaseManager = getattr(app.state, "db_manager", None)
    if db_manager:
        await db_manager.dispose()
    print("Database engine disposed")
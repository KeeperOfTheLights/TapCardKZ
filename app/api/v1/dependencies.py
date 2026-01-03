from fastapi import Request
from app.core.manager import AsyncDatabaseManager
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Retrieve the database session from the shared db_manager"""
    db_manager: AsyncDatabaseManager = request.app.state.db_manager
    async for session in db_manager.get_async_session():
        yield session
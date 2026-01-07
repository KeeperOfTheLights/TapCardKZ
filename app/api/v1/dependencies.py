from fastapi import Request
from app.core.manager import AsyncDatabaseManager
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from fastapi import HTTPException
from app.utils.jwt import jwt
from app.core.config import config

async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Retrieve the database session from the shared db_manager"""
    db_manager: AsyncDatabaseManager = request.app.state.db_manager
    async for session in db_manager.get_async_session():
        yield session

def verify_access_token(request: Request) -> dict | None:
    token: str | None = request.cookies.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token.split(" ")[1], config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")
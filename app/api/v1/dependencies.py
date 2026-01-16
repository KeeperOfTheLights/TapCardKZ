from typing import AsyncGenerator

import jose
from fastapi import Request, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.manager import AsyncDatabaseManager
from app import utils
from app.core import config

async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Retrieve the database session from the shared db_manager"""
    db_manager: AsyncDatabaseManager = request.app.state.db_manager
    async for session in db_manager.get_async_session():
        yield session

def verify_access_token(request: Request) -> dict | None:
    token: str | None = request.cookies.get("Authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = utils.token.verify(token.split(" ")[1])
        return payload
    except jose.JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

async def verify_admin(request: Request) -> dict | None:
    #TODO: implement admin verification
    token: str | None = request.cookies.get("Authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = jose.jwt.decode(token.split(" ")[1], config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        return payload
    except jose.JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
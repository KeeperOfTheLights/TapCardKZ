"""
API v1 dependencies.

Contains common dependency functions for routers.
"""
from typing import AsyncGenerator

import jose
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app import utils
from app.core.config import config
from app.core.manager import AsyncDatabaseManager


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session.
    
    Args:
        request: HTTP request with app state
        
    Yields:
        AsyncSession: Session for database operations
    """
    db_manager: AsyncDatabaseManager = request.app.state.db_manager
    async for session in db_manager.get_async_session():
        yield session


def verify_access_token(request: Request) -> dict | None:
    """
    Verify access token from cookie.
    
    Args:
        request: HTTP request
        
    Returns:
        dict: Token payload with card_id
        
    Raises:
        HTTPException: 401 if token is missing
        HTTPException: 403 if token is invalid
    """
    token: str | None = request.cookies.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not authenticated"
        )
    try:
        payload = utils.token.verify(token.split(" ")[1])
        return payload
    except jose.JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid token"
        )


async def verify_admin(
    api_key: str | None = Depends(APIKeyHeader(name="X-Admin-Key", auto_error=False))
) -> None:
    """
    Verify admin API key from header.
    
    In Swagger UI, click "Authorize" button and enter the admin key.
    
    Raises:
        HTTPException: 401 if key is missing
        HTTPException: 403 if key is invalid
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Admin key required. Use X-Admin-Key header."
        )
    if api_key != config.ADMIN_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid admin key"
        )
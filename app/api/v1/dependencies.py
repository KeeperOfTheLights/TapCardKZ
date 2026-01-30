"""
API v1 dependencies.

Contains common dependency functions for routers.
"""
from typing import AsyncGenerator

import jose
from fastapi import HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import utils
from app.core import config
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


async def verify_admin(request: Request) -> dict | None:
    """
    Verify admin token from cookie.
    
    Args:
        request: HTTP request
        
    Returns:
        dict: Admin token payload
        
    Raises:
        HTTPException: 401 if token is missing
        HTTPException: 403 if token is invalid
    """
    # TODO: implement admin verification
    token: str | None = request.cookies.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not authenticated"
        )
    try:
        payload = jose.jwt.decode(
            token.split(" ")[1], 
            config.JWT_SECRET, 
            algorithms=[config.JWT_ALGORITHM]
        )
        return payload
    except jose.JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid token"
        )
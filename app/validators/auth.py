"""
Authentication validators.

Check JWT token presence and validity.
"""
import jose
from fastapi import HTTPException, Request, status

from app import utils
from app.core import config


def require_access_token(request: Request) -> dict:
    """
    Verify access token in cookies.
    
    Args:
        request: HTTP request
        
    Returns:
        dict: Token payload with card_id
        
    Raises:
        HTTPException: 401 if token missing
        HTTPException: 403 if token invalid
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


def require_admin_token(request: Request) -> dict:
    """
    Verify admin token in cookies.
    
    Args:
        request: HTTP request
        
    Returns:
        dict: Admin token payload
        
    Raises:
        HTTPException: 401 if token missing
        HTTPException: 403 if token invalid
    """
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

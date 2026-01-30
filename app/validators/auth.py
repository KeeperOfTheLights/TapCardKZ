"""
Валидаторы для аутентификации.

Проверяют наличие и валидность JWT токенов.
"""
# Third-party
import jose
from fastapi import HTTPException, Request, status

# Local
from app import utils
from app.core import config


def require_access_token(request: Request) -> dict:
    """
    Проверяет наличие и валидность access token в cookies.
    
    Args:
        request: HTTP запрос
        
    Returns:
        dict: Payload токена с card_id
        
    Raises:
        HTTPException: 401 если токен отсутствует
        HTTPException: 403 если токен недействителен
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
    Проверяет наличие и валидность admin token в cookies.
    
    Args:
        request: HTTP запрос
        
    Returns:
        dict: Payload токена администратора
        
    Raises:
        HTTPException: 401 если токен отсутствует
        HTTPException: 403 если токен недействителен
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

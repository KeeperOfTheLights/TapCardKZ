from app.core.config import config
from datetime import datetime, timedelta
from jose import jwt
from fastapi import Request


def create(card_id: int) -> str:
    """
    Create new JWT token for card access.
    
    Args:
        card_id: Card ID to encode in token
        
    Returns:
        str: Encoded JWT token
    """
    expire = datetime.utcnow() + timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    
    payload = {
        "card_id": card_id,
        "exp": expire,
        "type": "edit_access"
    }
    
    token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return token


def verify(token: str) -> dict | None:
    """
    Verify JWT token and return payload.
    
    Args:
        token: JWT token to verify
        
    Returns:
        dict | None: Token payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        return payload
    except jwt.JWTError:
        return None


def get_or_create(request: Request, card_id: int) -> tuple[str, bool]:
    """
    Get existing valid token from cookies or create new one.
    
    Args:
        request: FastAPI request with cookies
        card_id: Card ID for token validation/creation
        
    Returns:
        tuple[str, bool]: (token, is_new) - token string and flag if token was newly created
    """
    # Проверяем наличие токена в куках
    cookie_token = request.cookies.get("Authorization")
    
    if cookie_token:
        # Извлекаем токен из формата "Bearer <token>"
        try:
            token_value = cookie_token.split(" ")[1] if " " in cookie_token else cookie_token
            payload = verify(token_value)
            
            # Если токен валиден и принадлежит нужной карточке - используем его
            if payload and payload.get("card_id") == card_id:
                return token_value, False
        except (IndexError, AttributeError):
            pass
    
    # Если токена нет или он невалиден - создаём новый
    new_token = create(card_id)
    return new_token, True
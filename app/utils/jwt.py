from datetime import datetime, timedelta
from jose import jwt

from app.core.config import config


def create_access_token(card_id: int) -> str:
    """
    Create a JWT token that grants edit access to a specific card.
    """
    expire = datetime.utcnow() + timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    
    payload = {
        "card_id": card_id,
        "exp": expire,
        "type": "edit_access"
    }
    
    token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return token


def verify_access_token(token: str) -> dict | None:
    """
    Verify a JWT token and return the payload if valid.
    Returns None if invalid or expired.
    """
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        return payload
    except jwt.JWTError:
        return None
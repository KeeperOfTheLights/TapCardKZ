from app.core.config import config
from datetime import datetime, timedelta
from jose import jwt

def create(card_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    
    payload = {
        "card_id": card_id,
        "exp": expire,
        "type": "edit_access"
    }
    
    token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return token


def verify(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        return payload
    except jwt.JWTError:
        return None
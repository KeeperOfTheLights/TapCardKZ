import secrets
import hashlib

from app.core.config import config


def generate() -> str:
    return secrets.token_urlsafe(config.CODE_LEN)

def encode(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()
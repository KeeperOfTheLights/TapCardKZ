import secrets
import hashlib

from app.core.config import config


def generate(length: int = config.CODE_LEN) -> str:
    return secrets.token_urlsafe(length)

def encode(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()
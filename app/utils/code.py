import secrets

def generate_code() -> str:
    return secrets.token_urlsafe(8)[:10]
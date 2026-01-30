"""
Валидаторы для кодов активации.

Проверяют существование и активность кода.
"""
# Third-party
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# Local
from app import repo
from app.core import models


async def require_active_code(code_hash: str, session: AsyncSession) -> models.Code:
    """
    Проверяет существование активного кода.
    
    Args:
        code_hash: Хеш кода для проверки
        session: Сессия БД
        
    Returns:
        models.Code: Найденный активный код
        
    Raises:
        HTTPException: 401 если код не найден или неактивен
    """
    code: models.Code | None = await repo.codes.get_active(
        code=code_hash, 
        session=session
    )
    if not code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid code or code not found"
        )
    return code

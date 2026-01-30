"""
Сервис для работы с кодами активации.

Содержит бизнес-логику активации и регенерации кодов.
"""
# Standard Library
import hashlib
import secrets

# Third-party
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

# Local
from app import repo, schemas, utils
from app.core import config, models


async def redeem(
    *,
    code_record: models.Code, 
    response: Response
) -> schemas.codes.Out:
    """
    Активировать код и вернуть JWT токен.
    
    Args:
        code_record: Провалидированный объект кода
        response: HTTP ответ для установки cookie
        
    Returns:
        schemas.codes.Out: Токен и ID карточки
    """
    access_token: str = utils.token.create(card_id=code_record.card_id)
    
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {access_token}",
        expires=config.JWT_EXPIRE_MINUTES * 60,
    )
    
    return schemas.codes.Out(
        access_token=access_token,
        token_type="bearer",
        card_id=code_record.card_id
    )


async def regenerate(
    *,
    card: models.Card,
    session: AsyncSession
) -> schemas.codes.RegenerateOut:
    """
    Регенерировать код для карточки.
    
    Args:
        card: Провалидированный объект карточки
        session: Сессия БД
        
    Returns:
        schemas.codes.RegenerateOut: Новый код активации
    """
    await repo.codes.deactivate(card_id=card.id, session=session)
    
    token: str = secrets.token_urlsafe(config.CODE_LEN)
    hashed_token: str = hashlib.sha256(token.encode()).hexdigest()
    
    code: models.Code = models.Code(
        card_id=card.id,
        code_hash=hashed_token,
        is_active=True
    )
    await repo.codes.add(code=code, session=session)
    
    return schemas.codes.RegenerateOut(
        card_id=card.id,
        code=token
    )
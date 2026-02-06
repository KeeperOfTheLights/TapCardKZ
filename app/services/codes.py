"""
Activation code service.

Contains business logic for code redemption and regeneration.
"""
from fastapi import Request, Response

from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, schemas, utils
from app.core import models
from app.core.config import config


async def redeem(
    code_record: models.Code,
    request: Request,
    response: Response
) -> schemas.codes.Out:
    """
    Redeem code and return JWT token.
    
    Checks if valid token already exists in cookies. If yes - reuses it.
    If no - creates new token.
    
    Args:
        code_record: Validated code object
        request: HTTP request (for reading cookies)
        response: HTTP response for setting cookie
        
    Returns:
        schemas.codes.Out: Token and card ID
    """
    # Получаем существующий токен или создаём новый
    token, is_new = utils.token.get_or_create(
        request=request,
        card_id=code_record.card_id
    )
    
    # Устанавливаем токен в куки (обновляем время жизни даже для существующего)
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {token}",
        expires=config.JWT_EXPIRE_MINUTES * 60,
        httponly=True,
        samesite="lax"
    )
    
    return schemas.codes.Out(
        access_token=token,
        token_type="bearer",
        card_id=code_record.card_id
    )


async def regenerate(
    card: models.Card, 
    session: AsyncSession
) -> schemas.codes.RegenerateOut:
    """
    Regenerate code for card.
    
    Args:
        card: Validated card object
        session: Database session
        
    Returns:
        schemas.codes.RegenerateOut: New activation code
    """
    generated_code: str = utils.code.generate()
    hashed_code: str = utils.code.encode(generated_code)
    
    await repo.codes.deactivate(card_id=card.id, session=session)
    code: models.Code = models.Code(
        card_id=card.id,
        code_hash=hashed_code,
        is_active=True
    )
    await repo.codes.create(code=code, session=session)
    
    return schemas.codes.RegenerateOut(
        card_id=card.id,
        code=generated_code
    )

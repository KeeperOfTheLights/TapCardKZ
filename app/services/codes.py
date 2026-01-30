"""
Activation code service.

Contains business logic for code redemption and regeneration.
"""
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, schemas, utils
from app.core import models
from app.core.config import config


async def redeem(
    code_record: models.Code, 
    response: Response
) -> schemas.codes.Out:
    """
    Redeem code and return JWT token.
    
    Args:
        code_record: Validated code object
        response: HTTP response for setting cookie
        
    Returns:
        schemas.codes.Out: Token and card ID
    """
    token: str = utils.token.create(card_id=code_record.card_id)
    
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {token}",
        expires=config.JWT_EXPIRE_MINUTES * 60
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
    code: str = utils.code.generate(config.CODE_LEN)
    hashed_code: str = utils.code.encode(code)
    
    await repo.codes.deactivate_all(card_id=card.id, session=session)
    await repo.codes.create(code=hashed_code, card_id=card.id, session=session)
    
    return schemas.codes.RegenerateOut(
        card_id=card.id,
        code=code
    )
import secrets
import hashlib

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Response

from app import schemas, utils, repo, utils
from app.core import config, models

async def redeem(
    *,
    code: schemas.codes.In, 
    session: AsyncSession,
    response: Response
) -> schemas.codes.Out:
    """
    Verify if the provided code exists and is active.
    If valid, return a JWT token for editing the card.
    """
    # 1. Find active code by code value (no card_id needed!)
    entered_code: str = code.code
    hashed_code: str = utils.code.encode(entered_code)
    code_record: models.Code | None = await repo.codes.get_active(code=hashed_code, session=session)

    # 2. Check if code exists
    if not code_record:
        raise HTTPException(
            status_code=401, 
            detail="Invalid code or code not found"
        )

    access_token: str = utils.token.create(card_id=code_record.card_id)
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {access_token}",
        expires=config.JWT_EXPIRE_MINUTES*60,
    )
    return schemas.codes.Out(
        access_token=access_token,
        token_type="bearer",
        card_id=code_record.card_id  # Return card_id so user knows which card
    )

async def regenerate(
    *,
    code: schemas.codes.RegenerateIn,
    session: AsyncSession
) -> schemas.codes.RegenerateOut:
    card: models.Card | None = await repo.cards.get(card_id=code.card_id, session=session)
    if not card:
        raise HTTPException(
            status_code=404,
            detail="Card not found"
        )
    await repo.codes.deactivate(card_id=code.card_id, session=session)
    token: str = secrets.token_urlsafe(config.CODE_LEN)
    hashed_token: str = hashlib.sha256(token.encode()).hexdigest()
    code: models.Code = models.Code(
        card_id=code.card_id,
        code_hash=hashed_token,
        is_active=True
    )
    await repo.codes.add(code=code, session=session)
    return schemas.codes.RegenerateOut(
        card_id=code.card_id,
        code=token
    )   
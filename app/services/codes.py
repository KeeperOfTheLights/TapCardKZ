from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Response

from app import schemas, utils, repo
from app.core import config, models
from app.utils.code import generate_code    


async def redeem(
    *,
    payload: schemas.codes.In, 
    session: AsyncSession,
    response: Response
) -> schemas.codes.Out:
    """
    Verify if the provided code exists and is active.
    If valid, return a JWT token for editing the card.
    """
    # 1. Find active code by code value (no card_id needed!)
    code_record: models.Code | None = await repo.codes.get_active_code(code=payload.code, session=session)

    # 2. Check if code exists
    if not code_record:
        raise HTTPException(
            status_code=401, 
            detail="Invalid code or code not found"
        )

    access_token: str = utils.jwt.create_access_token(card_id=code_record.card_id)
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
    payload: schemas.codes.RegenerateIn,
    session: AsyncSession
) -> schemas.codes.Out:
    card: models.Card | None = await repo.cards.get(card_id=payload.card_id, session=session)
    if not card:
        raise HTTPException(
            status_code=404,
            detail="Card not found"
        )
    await repo.codes.deactivate(card_id=payload.card_id, session=session)
    edit_token: str = generate_code()
    code: models.Code = models.Code(
        card_id=payload.card_id,
        code_hash=edit_token,
        is_active=True
    )
    await repo.codes.add(code=code, session=session)
    return schemas.codes.Out(
        access_token=edit_token,
        token_type="bearer",
        card_id=payload.card_id
    )   
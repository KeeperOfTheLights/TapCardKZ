from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Response

from app.core.models.code import Code
from app import schemas, utils, repo
from app.core.config import config
from sqlalchemy import update
from app.utils.code import generate_code    


async def redeem_code(
    *,
    payload: schemas.codes.CodeIn, 
    session: AsyncSession,
    response: Response
) -> schemas.codes.CodeOut:
    """
    Verify if the provided code exists and is active.
    If valid, return a JWT token for editing the card.
    """
    # 1. Find active code by code value (no card_id needed!)
    code_record: Code | None = await repo.codes.is_active_code(code=payload.code, session=session)

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
    return schemas.codes.CodeOut(
        access_token=access_token,
        token_type="bearer",
        card_id=code_record.card_id  # Return card_id so user knows which card
    )

async def regenerate_code(
    *,
    payload: schemas.codes.CodeIn,
    session: AsyncSession
) -> schemas.codes.CodeOut:
    await repo.codes.deactivate_codes(card_id=payload.card_id, session=session)
    edit_token: str = generate_code()
    code: Code = Code(
        card_id=payload.card_id,
        code_hash=edit_token,
        is_active=True
    )
    await repo.codes.add_code(code=code, session=session)
    return schemas.codes.CodeOut(
        access_token=edit_token,
        token_type="bearer",
        card_id=payload.card_id
    )   
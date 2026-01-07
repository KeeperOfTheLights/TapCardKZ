from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Response

from app.core.models.code import Code
from app.utils.jwt import create_access_token
from app import schemas
from app.core.config import config
from sqlalchemy import update
from app.utils.code import generate_code    

async def redeem_code(
    payload: schemas.codes.CodeRedeemIn, 
    session: AsyncSession,
    response: Response
) -> schemas.codes.CodeRedeemOut:
    """
    Verify if the provided code exists and is active.
    If valid, return a JWT token for editing the card.
    """
    # 1. Find active code by code value (no card_id needed!)
    query = select(Code).where(
        Code.is_active == True,
        Code.code_hash == payload.code  # Direct comparison (no hashing for now)
    )
    result = await session.execute(query)
    code_record = result.scalar_one_or_none()

    # 2. Check if code exists
    if not code_record:
        raise HTTPException(
            status_code=401, 
            detail="Invalid code or code not found"
        )

    access_token = create_access_token(card_id=code_record.card_id)
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {access_token}",
        expires=config.JWT_EXPIRE_MINUTES*60,
    )
    return schemas.codes.CodeRedeemOut(
        access_token=access_token,
        token_type="bearer",
        card_id=code_record.card_id  # Return card_id so user knows which card
    )

async def regenerate_code(
    payload: schemas.codes.RegenerateCodeIn,
    session: AsyncSession
) -> schemas.codes.CodeRegenerateOut:
    await session.execute(
        update(Code).where(Code.card_id == payload.card_id).values(is_active=False)
    )
    await session.commit()
    edit_token = generate_code()
    code = Code(
        card_id=payload.card_id,
        code_hash=edit_token,
        is_active=True
    )
    session.add(code)
    await session.commit()
    return schemas.codes.CodeRegenerateOut(
        code=edit_token,
        card_id=payload.card_id
    )   
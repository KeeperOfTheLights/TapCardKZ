from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.core.models.code import Code
from app.utils.jwt import create_access_token
from app import schemas


async def redeem_code(
    payload: schemas.codes.CodeRedeemIn, 
    session: AsyncSession
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

    # 3. Generate JWT token with the card_id from database
    access_token = create_access_token(card_id=code_record.card_id)

    return schemas.codes.CodeRedeemOut(
        access_token=access_token,
        token_type="bearer",
        card_id=code_record.card_id  # Return card_id so user knows which card
    )


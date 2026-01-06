from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.services import codes
from app.api.v1.dependencies import get_session

router = APIRouter(prefix="/codes", tags=["codes"])


@router.post("/redeem", response_model=schemas.codes.CodeRedeemOut)
async def redeem_code(
    payload: schemas.codes.CodeRedeemIn,
    session: AsyncSession = Depends(get_session)
) -> schemas.codes.CodeRedeemOut:
    """
    Verify a code and get a JWT token for editing the card.
    
    - **code**: The secret code received when creating the card
    
    Returns a JWT token and card_id that can be used to edit the card.
    """
    return await codes.redeem_code(payload, session)


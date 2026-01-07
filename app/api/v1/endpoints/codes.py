from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.services import codes
from app.api.v1.dependencies import get_session, verify_access_token

router = APIRouter(prefix="/codes", tags=["codes"])


@router.post("/redeem", response_model=schemas.codes.CodeRedeemOut)
async def redeem_code(
    payload: schemas.codes.CodeRedeemIn,
    response: Response,
    session: AsyncSession = Depends(get_session)
) -> schemas.codes.CodeRedeemOut:
    return await codes.redeem_code(payload, session, response)


#FOR ADMIN
@router.post("/regenerate", response_model=schemas.codes.CodeRegenerateOut)
async def regenerate_code(
    payload: schemas.codes.RegenerateCodeIn,
    session: AsyncSession = Depends(get_session)
) -> schemas.codes.CodeRegenerateOut:
    return await codes.regenerate_code(payload, session)
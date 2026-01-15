from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.services import codes
from app.api.v1.dependencies import get_session, verify_access_token

router: APIRouter = APIRouter(prefix="/codes")

@router.post("/redeem/", response_model=schemas.codes.CodeOut)
async def redeem_code(
    payload: schemas.codes.CodeIn,
    response: Response,
    session: AsyncSession = Depends(get_session)
) -> schemas.codes.CodeOut:
    return await codes.redeem_code(payload=payload, session=session, response=response)

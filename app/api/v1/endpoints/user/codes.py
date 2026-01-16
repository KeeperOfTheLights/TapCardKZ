from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services
from app.api.v1.dependencies import get_session, verify_access_token

router: APIRouter = APIRouter(prefix="/codes")

@router.post("/redeem/", response_model=schemas.codes.Out)
async def redeem_code(
    payload: schemas.codes.In,
    response: Response,
    session: AsyncSession = Depends(get_session)
) -> schemas.codes.Out:
    return await services.codes.redeem(payload=payload, session=session, response=response)

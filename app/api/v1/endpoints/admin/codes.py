from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_session, verify_admin
from app import schemas, services   

router: APIRouter = APIRouter(prefix="/codes")

@router.post("/regenerate/", response_model=schemas.codes.CodeOut)
async def regenerate_code(
    request: Request,
    payload: schemas.codes.CodeRegenerateIn,
    session: AsyncSession = Depends(get_session),
    #admin: dict = Depends(verify_admin)
) -> schemas.codes.CodeOut:
    return await services.codes.regenerate_code(payload=payload, session=session)
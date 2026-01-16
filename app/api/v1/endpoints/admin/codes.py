from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.dependencies import get_session, verify_admin
from app import schemas, services   

router: APIRouter = APIRouter(prefix="/codes")

@router.post("/regenerate/", response_model=schemas.codes.Out)
async def regenerate_code(
    code: schemas.codes.RegenerateIn,
    session: AsyncSession = Depends(get_session),
    #admin: dict = Depends(verify_admin)
) -> schemas.codes.Out:
    return await services.codes.regenerate(code=code, session=session)
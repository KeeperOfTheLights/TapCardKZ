from fastapi import APIRouter, Depends, Request, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_session, verify_access_token
from app import schemas, services

router: APIRouter = APIRouter(prefix="/socials")

@router.post("/", response_model=schemas.socials.Out)
async def create_social(
    social: schemas.socials.In,
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(verify_access_token)
) -> schemas.socials.Out:
    return await services.socials.create(
        card_id=token["card_id"], 
        social=social, 
        session=session,

    )

@router.delete("/{social_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_social(
    request: Request,
    social_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(verify_access_token)
):
    return await services.socials.delete(
        card_id=token["card_id"], 
        social_id=social_id, 
        session=session, 
        s3_client=request.app.state.s3_client
    )

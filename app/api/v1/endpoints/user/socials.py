from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_session, verify_access_token
from app import schemas, services

router: APIRouter = APIRouter(prefix="/socials")

@router.post("/", response_model=schemas.socials.SocialOut)
async def create_social(
    social: schemas.socials.SocialIn,
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(verify_access_token)
) -> schemas.socials.SocialOut:
    return await services.socials.create_social(card_id=token["card_id"], social=social, session=session)

@router.delete("/{social_id}/")
async def delete_social(
    social_id: int,
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(verify_access_token)
):
    return await services.socials.delete_social(card_id=token["card_id"], social_id=social_id, session=session)

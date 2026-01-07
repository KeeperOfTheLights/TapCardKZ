from fastapi import APIRouter, Depends, Request
from app.api.v1.dependencies import get_session
from app.services import socials
from app import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.dependencies import verify_access_token

router = APIRouter(prefix="/socials")

@router.post("/", response_model=schemas.socials.SocialOut)
async def create_social(
    social: schemas.socials.SocialIn,
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(verify_access_token)
) -> schemas.socials.SocialOut:
    return await socials.create_social(token["card_id"], social, session)

@router.delete("/{social_id}")
async def delete_social(
    social_id: int,
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(verify_access_token)
):
    return await socials.delete_social(token["card_id"], social_id, session)

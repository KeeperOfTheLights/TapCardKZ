
from app import schemas, repo
from app.core import models
from app.s3 import S3Client
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import delete   


async def create(   
    *, 
    card_id: int,
    social: schemas.socials.In,
    session: AsyncSession
) -> schemas.socials.Out:
    # 1. Загружаем карту сразу вместе с соцсетями
    card: models.Card | None = await repo.cards.get(card_id=card_id, session=session)
    
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card with id {card_id} not found"
        )
    card_social: models.socials.Out = await repo.socials.create(card=card, social=social, session=session)
    
    return schemas.socials.Out.model_validate(card_social, from_attributes=True)

async def delete(
    *,
    card_id: int,
    social_id: int,
    session: AsyncSession,
    s3_client: S3Client
) -> None:
    exist: bool = await repo.socials.is_exist(card_id=card_id, social_id=social_id, session=session)
    if not exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Social does not exist")

    social: models.CardSocial | None = await repo.socials.get(card_id=card_id, social_id=social_id, session=session)
    if social.card_id != card_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This social doesn't belong to this card")


    card: models.Card = await repo.cards.get(card_id=card_id, session=session)
    is_deleted: bool = await repo.socials.delete(card=card, social_id=social_id, session=session)
    
    if social.icon_asset_id:
        await s3_client.delete_social_asset(card_id=card_id, social_id=social_id)
    
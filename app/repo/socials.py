from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select

from app.core import models
from app import schemas

async def is_exist(
    *, 
    card_id: int,
    social_id: int,
    session: AsyncSession
) -> bool:
    stmt = select(models.CardSocial).where(
        models.CardSocial.card_id == card_id,
        models.CardSocial.id == social_id
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None

async def get(
    *, 
    card_id: int,
    social_id: int,
    session: AsyncSession
) -> models.CardSocial | None:
    stmt = select(models.CardSocial).where(
        models.CardSocial.card_id == card_id,
        models.CardSocial.id == social_id
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create(
    *, 
    card: models.Card, 
    social: schemas.socials.In,
    session: AsyncSession
) -> models.CardSocial:
    card_social: models.CardSocial = models.CardSocial(**social.model_dump())
    card.socials.append(card_social)
    await session.commit()
    await session.refresh(card_social)
    return card_social

async def delete(
    *, 
    card: models.Card, 
    social_id: int, 
    session: AsyncSession
) -> bool:
    target_social = next((s for s in card.socials if s.id == social_id), None)
    if target_social:
        card.socials.remove(target_social)
        await session.commit()
        return True
    return False
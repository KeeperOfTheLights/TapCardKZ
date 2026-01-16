from app.core import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get(
    *, 
    card_id: int, 
    session: AsyncSession
) -> models.Card | None:
    query = (
        select(models.Card)
        .where(models.Card.id == card_id)
        .options(selectinload(models.Card.socials)) 
    )
    result = await session.execute(query)
    card = result.scalar_one_or_none()
    return card

async def add(
    *, 
    card: models.Card, 
    session: AsyncSession
) -> models.Card:
    session.add(card)
    await session.commit()
    await session.refresh(card)
    return card
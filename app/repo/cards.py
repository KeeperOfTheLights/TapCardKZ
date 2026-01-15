from app.core.models.card import Card
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_card(*, card_id: int, session: AsyncSession) -> Card | None:
    query = (
        select(Card)
        .where(Card.id == card_id)
        .options(selectinload(Card.socials)) 
    )
    result = await session.execute(query)
    card = result.scalar_one_or_none()
    return card

async def add_card(*, card: Card, session: AsyncSession) -> Card:
    session.add(card)
    await session.commit()
    await session.refresh(card)
    return card
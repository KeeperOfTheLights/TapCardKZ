from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models.card import Card
from app import schemas
from sqlalchemy import select
from fastapi import HTTPException

from sqlalchemy.orm import selectinload

async def get_card(id: int, session: AsyncSession) -> schemas.cards.CardOut:
    query = (
        select(Card)
        .where(Card.id == id)
        .options(selectinload(Card.socials)) 
    )
    
    result = await session.execute(query)
    card: Card | None = result.scalar_one_or_none()

    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    return schemas.cards.CardOut.model_validate(card, from_attributes=True)

async def create_card(payload: schemas.cards.CardIn, session: AsyncSession) -> schemas.cards.CardOut:
    card = Card(**payload.model_dump())
    session.add(card)
    await session.commit()

    stmt = (
        select(Card)
        .where(Card.id == card.id)
        .options(selectinload(Card.socials))
    )
    res = await session.execute(stmt)

    card: Card = res.scalar_one()

    return schemas.cards.CardOut.model_validate(card, from_attributes=True)
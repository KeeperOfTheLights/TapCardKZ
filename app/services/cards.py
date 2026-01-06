from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models.card import Card
from app.core.models.code import Code
from app import schemas
from sqlalchemy import select
from fastapi import HTTPException

from sqlalchemy.orm import selectinload

from app.utils import generate_code


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
    # 1. Create the card
    card = Card(**payload.model_dump())
    session.add(card)
    await session.flush()  # Get card.id without committing

    # 2. Generate edit token and create code
    edit_token = generate_code()
    code = Code(
        card_id=card.id,
        code_hash=edit_token,
        is_active=True
    )
    session.add(code)

    # 3. Commit both
    await session.commit()

    # 4. Reload card with relationships
    stmt = (
        select(Card)
        .where(Card.id == card.id)
        .options(selectinload(Card.socials))
    )
    res = await session.execute(stmt)
    card: Card = res.scalar_one()

    # 5. Return card with token
    card_out = schemas.cards.CardOut.model_validate(card, from_attributes=True)
    return schemas.cards.CardOutWithEditToken(
        **card_out.model_dump(),
        edit_token=edit_token
    )
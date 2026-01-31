"""
Card validators.

Check card existence and return it or raise HTTPException.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo
from app.core import models


async def require_card(card_id: int, session: AsyncSession) -> models.Card:
    """
    Verify card existence.
    
    Args:
        card_id: Card ID to check
        session: Database session
        
    Returns:
        models.Card: Found card
        
    Raises:
        HTTPException: 404 if card not found
    """
    card: models.Card | None = await repo.cards.get(card_id=card_id, session=session)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card with id {card_id} not found"
        )
    return card

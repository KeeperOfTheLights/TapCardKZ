"""
Валидаторы для карточек.

Проверяют существование карточки и возвращают её или выбрасывают HTTPException.
"""
# Third-party
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# Local
from app import repo
from app.core import models


async def require_card(card_id: int, session: AsyncSession) -> models.Card:
    """
    Проверяет существование карточки.
    
    Args:
        card_id: ID карточки для проверки
        session: Сессия БД
        
    Returns:
        models.Card: Найденная карточка
        
    Raises:
        HTTPException: 404 если карточка не найдена
    """
    card: models.Card | None = await repo.cards.get(card_id=card_id, session=session)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card with id {card_id} not found"
        )
    return card

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo
from app.core import models


async def require_social(
    card_id: int, 
    social_id: int, 
    session: AsyncSession
) -> models.CardSocial:
    """
    Проверяет существование соцсети и принадлежность к карточке.
    
    Args:
        card_id: ID карточки-владельца
        social_id: ID социальной сети
        session: Сессия БД
        
    Returns:
        models.CardSocial: Найденная социальная сеть
        
    Raises:
        HTTPException: 404 если соцсеть не найдена или не принадлежит карточке
    """
    social: models.CardSocial | None = await repo.socials.get(
        card_id=card_id, 
        social_id=social_id, 
        session=session
    )
    if not social:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Social not found"
        )
    if social.card_id != card_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Social doesn't belong to this card"
        )
    return social


def require_no_icon(social: models.CardSocial) -> None:
    """
    Проверяет, что у соцсети ещё нет кастомной иконки.
    
    Args:
        social: Социальная сеть для проверки
        
    Raises:
        HTTPException: 400 если иконка уже существует
    """
    if social.icon_asset_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="App icon already exists"
        )

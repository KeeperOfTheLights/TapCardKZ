"""
Social link validators.

Check social link existence and ownership.
"""
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
    Verify social link existence and ownership.
    
    Args:
        card_id: Owner card ID
        social_id: Social link ID
        session: Database session
        
    Returns:
        models.CardSocial: Found social link
        
    Raises:
        HTTPException: 404 if not found or doesn't belong to card
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
    Verify social link has no custom icon.
    
    Args:
        social: Social link to check
        
    Raises:
        HTTPException: 400 if icon already exists
    """
    if social.icon_asset_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="App icon already exists"
        )

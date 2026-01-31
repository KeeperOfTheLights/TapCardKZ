"""
Social link service.

Contains business logic for creating and deleting social links.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, schemas
from app.core import models
from app.core.config import config
from app.s3.client import S3Client


async def create(
    card: models.Card, 
    social: schemas.socials.In, 
    session: AsyncSession
) -> schemas.socials.Out:
    """
    Create social link for card.
    
    Args:
        card: Validated card object
        social: Social link data
        session: Database session
        
    Returns:
        schemas.socials.Out: Created social link
    """
    card_social: models.socials.Out = await repo.socials.create(card=card, social=social, session=session)
    
    return schemas.socials.Out.model_validate(card_social, from_attributes=True)


async def delete(
    social: models.CardSocial, 
    card: models.Card, 
    session: AsyncSession, 
    s3_client: S3Client
) -> None:
    """
    Delete social link and associated icon.
    
    Args:
        social: Validated social link object
        card: Card object
        session: Database session
        s3_client: S3 client for deleting icon
    """
    await repo.socials.delete(card=card, social_id=social.id, session=session)
    
    if social.icon_asset_id:
        file_name: str = config.S3_ICON_TEMPLATE.format(card_id=card.id, social_id=social.id)
        await s3_client.delete_asset(file_name=file_name)
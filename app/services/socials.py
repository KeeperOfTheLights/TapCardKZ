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
    social_record: models.CardSocial = await repo.socials.create(
        card=card, 
        social=social, 
        session=session
    )
    
    return schemas.socials.Out(
        id=social_record.id,
        card_id=card.id,
        type=social_record.type,
        url=social_record.url,
        label=social_record.label,
        order_id=social_record.order_id,
        icon_asset_id=social_record.icon_asset_id,
        is_visible=social_record.is_visible,
        created_at=social_record.created_at,
        app_icon_link=None
    )


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
    if social.icon_asset_id:
        icon: models.Asset | None = await repo.logos.get(
            asset_id=social.icon_asset_id, 
            session=session
        )
        if icon:
            await s3_client.delete_file(
                object_name=config.S3_ICON_TEMPLATE.format(
                    card_id=card.id,
                    file_name=icon.file_name
                )
            )
            await repo.logos.delete(asset=icon, session=session)
    
    await repo.socials.delete(social=social, session=session)
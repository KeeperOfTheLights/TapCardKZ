"""
Social link icon service.

Contains business logic for getting and uploading icons.
"""
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, schemas
from app.core import enums, models
from app.core.config import config
from app.s3.client import S3Client


async def get_all(
    card_id: int, 
    s3_client: S3Client, 
    session: AsyncSession
) -> dict[int, str]:
    """
    Get all icons for card.
    
    Args:
        card_id: Card ID
        s3_client: S3 client for getting URLs
        session: Database session
        
    Returns:
        dict[int, str]: Mapping of social_id to icon URL
    """
    # Get socials with their icon asset IDs
    asset_names: dict[int, str] = await repo.logos.get_all(card_id=card_id, session=session)
    if not asset_names:
        return {}
    asset_urls: dict[int, str] = {
        asset_id: await s3_client.get_object_url(
            asset_names.get(asset_id)
        )
        for asset_id in asset_names.keys()
    }
    
    return asset_urls




async def upload(
    social: models.CardSocial, 
    s3_client: S3Client, 
    file: UploadFile, 
    session: AsyncSession
) -> schemas.assets.Out:
    """
    Upload icon for social link.
    
    Args:
        social: Validated social link object
        s3_client: S3 client for upload
        file: Image file
        session: Database session
        
    Returns:
        schemas.assets.Out: Uploaded asset info
    """
    file_name: str = config.S3_ICON_TEMPLATE.format(
        card_id=social.card_id,
        social_id=social.id
    )
    asset: models.CardAsset = await repo.logos.create(
        card_id=social.card_id, 
        social_id=social.id,
        file_name=file_name, 
        session=session
    )
    await s3_client.upload_file(
        file_obj=file,
        object_name=file_name
    )
    
    return schemas.assets.Out.model_validate(asset, from_attributes=True)

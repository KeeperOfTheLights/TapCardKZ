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
    icons: list[models.Asset] = await repo.logos.get_all(
        card_id=card_id, 
        session=session
    )
    
    socials: list[models.CardSocial] = await repo.socials.get_all(
        card_id=card_id, 
        session=session
    )
    
    icon_dict: dict[int, str] = {}
    for icon in icons:
        social = next(
            (s for s in socials if s.icon_asset_id == icon.id), 
            None
        )
        if social:
            icon_dict[social.id] = s3_client.create_presigned_url(
                object_name=config.S3_ICON_TEMPLATE.format(
                    card_id=card_id,
                    file_name=icon.file_name
                ),
                expires_in=config.IMAGE_EXPIRE_TIME
            )
    
    return icon_dict


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
    asset: models.Asset = await repo.logos.set(
        social=social, 
        file_name=file.filename, 
        session=session
    )
    
    await s3_client.upload_file(
        file=file,
        object_name=config.S3_ICON_TEMPLATE.format(
            card_id=social.card_id,
            file_name=file.filename
        )
    )
    
    return schemas.assets.Out(
        id=asset.id,
        card_id=social.card_id,
        type=enums.AssetType.ICON,
        file_name=file.filename,
        created_at=asset.created_at
    )

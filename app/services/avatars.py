"""
Avatar service.

Contains business logic for getting and uploading avatars.
"""
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, schemas
from app.core import enums, models
from app.core.config import config
from app.s3.client import S3Client


async def get(
    card_id: int, 
    s3_client: S3Client, 
    session: AsyncSession
) -> str | None:
    """
    Get avatar URL for card.
    
    Args:
        card_id: Card ID
        s3_client: S3 client for getting URL
        session: Database session
        
    Returns:
        str | None: Avatar URL or None
    """
    avatar_asset: models.Asset | None = await repo.avatars.get(
        card_id=card_id, 
        session=session
    )
    if not avatar_asset:
        return None
    
    file_name: str = config.S3_AVATAR_TEMPLATE.format(card_id=card_id)
    return await s3_client.get_object_url(object_name=file_name)


async def upload(
    card: models.Card, 
    s3_client: S3Client, 
    file: UploadFile, 
    session: AsyncSession
) -> schemas.assets.Out:
    """
    Upload avatar for card.
    
    Args:
        card: Validated card object
        s3_client: S3 client for upload
        file: Image file
        session: Database session
        
    Returns:
        schemas.assets.Out: Uploaded asset info
    """
    file_name: str = config.S3_AVATAR_TEMPLATE.format(card_id=card.id)
    asset: models.Asset = await repo.avatars.create(
        card_id=card.id, 
        file_name=file_name, 
        session=session
    )
    await s3_client.upload_file(file_obj=file, object_name=file_name)
    
    return schemas.assets.Out.model_validate(asset, from_attributes=True)
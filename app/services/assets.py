from fastapi import HTTPException, status, UploadFile
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.s3.client import S3Client
from app.core.config import config
from app.core.models.card import Card
from app import schemas, repo
from app.core.models.asset import AssetType, CardAsset
from app.core.models.social import CardSocial


async def image_validator(
    *, 
    card_id: int, 
    file: UploadFile, 
    session: AsyncSession,
    max_size: int = config.IMAGE_MAX_SIZE,
    allowed_types: list[str] = config.ALLOWED_IMAGE_TYPES
) -> None:
    if file.size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Too large file, it must be less than 5MB"
        )

    card: Card | None = await session.get(Card, card_id)
    if not card:
        raise HTTPException(    
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card with id {card_id} not found"
        )

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not allowed file type, allowed types: {', '.join(allowed_types)}"
        )


async def get_avatar(
    *,
    card_id: int, 
    s3_client: S3Client, 
    session: AsyncSession
) -> str | None:
    filename: str = f"avatar-{card_id}.png"
    asset: CardAsset | None = await repo.assets.find_avatar(card_id=card_id, session=session)
    if not asset:
        return None 
    return await s3_client.get_object_url(filename)


async def get_logos(
    *,
    card_id: int, 
    s3_client: S3Client, 
    session: AsyncSession
) -> list[schemas.assets.LogoLinksOut]:
    assets: list[CardAsset] = await repo.assets.find_logos(card_id=card_id, session=session)
    
    if not assets:
        return []
    
    return [
        schemas.assets.LogoLinksOut(
            order_id=asset.order_id,
            link=await s3_client.get_object_url(asset.file_name)
        )
        for asset in assets
    ]

async def upload_avatar(
    *,
    card_id: int, 
    s3_client: S3Client,
    file: UploadFile, 
    session: AsyncSession
):
    file_name: str = f"avatar-{card_id}.png"
    await image_validator(card_id=card_id, file=file, session=session)
    asset: CardAsset = await repo.assets.add_avatar(card_id=card_id, file_name=file_name, session=session)

    await s3_client.upload_file(file.file, file_name)
    return schemas.assets.AssetOut.model_validate(asset, from_attributes=True)

async def upload_logo(
    *,
    card_id: int, 
    social_id: int,
    s3_client: S3Client,
    file: UploadFile, 
    session: AsyncSession
):
    file_name: str = f"app_icon-{card_id}-{social_id}.png"
    await image_validator(card_id=card_id, file=file, session=session)
    try:
        asset: CardAsset | None = await repo.assets.upload_logo(card_id=card_id, social_id=social_id, file_name=file_name, session=session)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="App icon already exists")
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Social not found")
    await s3_client.upload_file(file.file, file_name)
    return schemas.assets.AssetOut.model_validate(asset, from_attributes=True)

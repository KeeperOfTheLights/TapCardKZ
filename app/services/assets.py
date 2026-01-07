from app.core.models.asset import CardAsset
from app.s3.client import S3Client
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import config
from app.core.models.card import Card
from app import schemas
from fastapi import HTTPException, status, UploadFile
from sqlalchemy import delete
from app.core.models.asset import AssetType
from sqlalchemy import select, update
from app.core.models.asset import CardAsset
from app.core.models.card import Card
from app.core.models.social import CardSocial
from sqlalchemy.exc import IntegrityError

async def image_validator(file: UploadFile, session: AsyncSession, card_id: int):
    max_size: int = config.IMAGE_MAX_SIZE
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

    allowed_types: list[str] = config.ALLOWED_IMAGE_TYPES
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not allowed file type, allowed types: {', '.join(allowed_types)}"
        )

async def get_avatar(card_id: int, s3_client: S3Client, session: AsyncSession) -> str | None:
    filename: str = f"avatar-{card_id}.png"
    result = await session.execute(select(CardAsset).where(CardAsset.card_id == card_id).where(CardAsset.type == AssetType.avatar))
    asset = result.scalar_one_or_none()
    if not asset:
        return None
    
    avatar_link: str | None = await s3_client.get_object_url(filename)
    return avatar_link

async def get_logos(card_id: int, s3_client: S3Client, session: AsyncSession) -> dict[int, str]:
    # Убираем .order_by(CardAsset.order_id), так как его не существует
    stmt = (
        select(CardAsset)
        .where(CardAsset.card_id == card_id)
        .where(CardAsset.type == AssetType.app_icon)
    )
    result = await session.execute(stmt)
    assets = result.scalars().all()
    
    if not assets:
        return {}
    
    # Возвращаем словарь, где ключ — ID картинки, а значение — ссылка
    return {
        asset.id: await s3_client.get_object_url(asset.file_name) 
        for asset in assets
    }

async def upload_avatar(
    card_id: int, 
    s3_client: S3Client,
    file: UploadFile, 
    session: AsyncSession
):
    file_name: str = f"avatar-{card_id}.png"
    await image_validator(file, session, card_id)
    await session.execute(
        delete(CardAsset).where(CardAsset.card_id == card_id).where(CardAsset.type == AssetType.avatar)
    )
    await session.commit()
    

    asset: CardAsset = CardAsset(card_id=card_id, type=AssetType.avatar, file_name=file_name)
    session.add(asset)
    await session.commit()
    await session.refresh(asset)

    await s3_client.upload_file(file.file, file_name)
    return schemas.assets.AssetOut.model_validate(asset, from_attributes=True)

async def upload_logo(
    card_id: int, 
    social_id: int,
    s3_client: S3Client,
    file: UploadFile, 
    session: AsyncSession
):
    file_name: str = f"app_icon-{card_id}-{social_id}.png"
    result = await session.execute(select(CardSocial).where(CardSocial.id == social_id).where(CardSocial.card_id == card_id))
    social = result.scalar_one_or_none()
    if not social:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Social not found")
    await image_validator(file, session, card_id)
    asset: CardAsset = CardAsset(card_id=card_id, type=AssetType.app_icon, file_name=file_name)
    try:
        session.add(asset)
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="App icon already exists")
    await session.refresh(asset)
    await session.execute(
        update(CardSocial).where(CardSocial.id == social_id).where(CardSocial.card_id == card_id).values(icon_asset_id=asset.id)
    )

    await session.commit()
    await s3_client.upload_file(file.file, file_name)
    return schemas.assets.AssetOut.model_validate(asset, from_attributes=True)

from app.core import models, enums
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all(
    *, 
    card_id: int,
    session: AsyncSession
) -> dict[int, str] | None:
    stmt = (
        select(models.CardAsset)
        .where(models.CardAsset.card_id == card_id)
        .where(models.CardAsset.type == enums.AssetType.app_icon)
    )
    result = await session.execute(stmt)
    assets = result.scalars().all()
    return {asset.id: asset.file_name for asset in assets}

async def create(
    *, 
    card_id: int,
    social_id: int,
    file_name: str,
    session: AsyncSession
) -> models.CardAsset | None:
    result = await session.execute(
        select(models.CardSocial)
        .where(models.CardSocial.id == social_id)
        .where(models.CardSocial.card_id == card_id)
    )
    social: models.CardSocial | None = result.scalar_one_or_none()
    if not social:
        return None
    asset: models.CardAsset = models.CardAsset(card_id=card_id, type=enums.AssetType.app_icon, file_name=file_name)
    session.add(asset)
    await session.commit()
    await session.refresh(asset)
    await session.execute(
        update(models.CardSocial)
        .where(models.CardSocial.id == social_id)
        .where(models.CardSocial.card_id == card_id)
        .values(icon_asset_id=asset.id)
    )
    await session.commit()
    return asset
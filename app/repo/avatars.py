from app.core import models, enums

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

async def get(
    *,
    card_id: int,
    session: AsyncSession
) -> models.CardAsset | None:
    result = await session.execute(
        select(models.CardAsset)
        .where(models.CardAsset.card_id == card_id)
        .where(models.CardAsset.type == enums.AssetType.avatar)
    )
    asset: models.CardAsset | None = result.scalar_one_or_none()
    return asset


async def create(
    *, 
    card_id: int,
    file_name: str,
    session: AsyncSession
) -> models.CardAsset:
    await session.execute(
        delete(models.CardAsset)
        .where(models.CardAsset.card_id == card_id)
        .where(models.CardAsset.type == enums.AssetType.avatar)
    )
    await session.commit()

    asset: models.CardAsset = models.CardAsset(card_id=card_id, type=enums.AssetType.avatar, file_name=file_name)
    session.add(asset)
    await session.commit()
    await session.refresh(asset)
    return asset
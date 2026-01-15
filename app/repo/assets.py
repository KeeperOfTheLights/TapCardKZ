from app.core.models.asset import CardAsset, AssetType
from app.core.models.social import CardSocial
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

async def get_avatar(*, card_id: int, session: AsyncSession) -> CardAsset | None:
    result = await session.execute(select(CardAsset).where(CardAsset.card_id == card_id).where(CardAsset.type == AssetType.avatar))
    asset = result.scalar_one_or_none()
    return asset

async def get_logos(*, card_id: int, session: AsyncSession) -> dict[int, str] | None:
    stmt = (
        select(CardAsset)
        .where(CardAsset.card_id == card_id)
        .where(CardAsset.type == AssetType.app_icon)
    )
    result = await session.execute(stmt)
    assets = result.scalars().all()
    return {asset.id: asset.file_name for asset in assets}

async def add_avatar(*, card_id: int, file_name: str, session: AsyncSession) -> CardAsset:
    await session.execute(
        delete(CardAsset).where(CardAsset.card_id == card_id).where(CardAsset.type == AssetType.avatar)
    )
    await session.commit()

    asset: CardAsset = CardAsset(card_id=card_id, type=AssetType.avatar, file_name=file_name)
    session.add(asset)
    await session.commit()
    await session.refresh(asset)
    return asset

async def upload_logo(*, card_id: int, social_id: int, file_name: str, session: AsyncSession) -> CardAsset | None:
    result = await session.execute(select(CardSocial).where(CardSocial.id == social_id).where(CardSocial.card_id == card_id))
    social: CardSocial | None = result.scalar_one_or_none()
    if not social:
        return None
    asset: CardAsset = CardAsset(card_id=card_id, type=AssetType.app_icon, file_name=file_name)
    session.add(asset)
    await session.commit()
    await session.refresh(asset)
    await session.execute(
        update(CardSocial)
        .where(CardSocial.id == social_id)
        .where(CardSocial.card_id == card_id)
        .values(icon_asset_id=asset.id)
    )
    await session.commit()
    return asset
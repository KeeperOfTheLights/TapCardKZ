from fastapi import HTTPException, status, UploadFile
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.s3 import S3Client
from app import schemas, repo
from app.core import models, config
from app.utils import utils

async def get(
    *,
    card_id: int, 
    s3_client: S3Client, 
    session: AsyncSession
) -> dict[int, str]:
    assets: list[models.CardAsset] = await repo.logos.get(card_id=card_id, session=session)
    
    if not assets:
        return {}
    
    return {
        asset.order_id: await s3_client.get_object_url(asset.file_name)
        for asset in assets
    }


async def upload(
    *,
    card_id: int, 
    social_id: int,
    s3_client: S3Client,
    file: UploadFile, 
    session: AsyncSession
) -> schemas.assets.Out:
    social: models.CardSocial | None = await repo.socials.get(card_id=card_id, social_id=social_id, session=session)
    if not social:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Social not found or does not belong to this card")
    if social.icon_asset_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="App icon already exists")
    file_name: str = config.S3_ICON_TEMPLATE.format(card_id=card_id, social_id=social_id)
    await utils.image_validator(card_id=card_id, file=file, session=session)
    asset: models.CardAsset = await repo.logos.add(card_id=card_id, social_id=social_id, file_name=file_name, session=session)
    await s3_client.upload_file(file.file, file_name)
    return schemas.assets.Out.model_validate(asset, from_attributes=True)

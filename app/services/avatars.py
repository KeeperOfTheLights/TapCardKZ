from app.core import models
from app import repo, schemas
from app.s3 import S3Client
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from app.utils import utils

async def get(
    *,
    card_id: int, 
    s3_client: S3Client, 
    session: AsyncSession
) -> str | None:
    filename: str = f"avatar-{card_id}.png"
    asset: models.CardAsset | None = await repo.avatars.get(card_id=card_id, session=session)
    if not asset:
        return None 
    return await s3_client.get_object_url(filename)

async def upload(
    *,
    card_id: int, 
    s3_client: S3Client,
    file: UploadFile, 
    session: AsyncSession
) -> schemas.assets.Out:
    file_name: str = f"avatar-{card_id}.png"
    await utils.image_validator(card_id=card_id, file=file, session=session)
    asset: models.CardAsset = await repo.avatars.add(card_id=card_id, file_name=file_name, session=session)

    await s3_client.upload_file(file.file, file_name)
    return schemas.assets.Out.model_validate(asset, from_attributes=True)
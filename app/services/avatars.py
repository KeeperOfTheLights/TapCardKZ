"""
Сервис для работы с аватарами.

Содержит бизнес-логику получения и загрузки аватаров.
"""
# Third-party
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

# Local
from app import repo, schemas
from app.core import config, models
from app.s3 import S3Client


async def get(
    *,
    card_id: int, 
    s3_client: S3Client, 
    session: AsyncSession
) -> str | None:
    """
    Получить URL аватара для карточки.
    
    Args:
        card_id: ID карточки
        s3_client: Клиент S3 для получения URL
        session: Сессия БД
        
    Returns:
        str | None: URL аватара или None
    """
    filename: str = config.S3_AVATAR_TEMPLATE.format(card_id=card_id)
    
    asset: models.CardAsset | None = await repo.avatars.get(
        card_id=card_id, 
        session=session
    )
    
    if not asset:
        return None 
    
    return await s3_client.get_object_url(filename)


async def upload(
    *,
    card: models.Card, 
    s3_client: S3Client,
    file: UploadFile, 
    session: AsyncSession
) -> schemas.assets.Out:
    """
    Загрузить аватар для карточки.
    
    Args:
        card: Провалидированный объект карточки
        s3_client: Клиент S3 для загрузки
        file: Файл изображения
        session: Сессия БД
        
    Returns:
        schemas.assets.Out: Информация о загруженном ассете
    """
    file_name: str = config.S3_AVATAR_TEMPLATE.format(card_id=card.id)
    
    asset: models.CardAsset = await repo.avatars.add(
        card_id=card.id, 
        file_name=file_name, 
        session=session
    )
    
    await s3_client.upload_file(file.file, file_name)
    
    return schemas.assets.Out.model_validate(asset, from_attributes=True)
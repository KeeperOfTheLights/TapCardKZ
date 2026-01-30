"""
Сервис для работы с логотипами социальных сетей.

Содержит бизнес-логику получения и загрузки иконок.
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
) -> dict[int, str]:
    """
    Получить все логотипы для карточки.
    
    Args:
        card_id: ID карточки
        s3_client: Клиент S3 для получения URL
        session: Сессия БД
        
    Returns:
        dict[int, str]: Словарь {order_id: url}
    """
    assets: list[models.CardAsset] = await repo.logos.get(
        card_id=card_id, 
        session=session
    )
    
    if not assets:
        return {}
    
    return {
        asset.order_id: await s3_client.get_object_url(asset.file_name)
        for asset in assets
    }


async def upload(
    *,
    social: models.CardSocial,
    s3_client: S3Client,
    file: UploadFile, 
    session: AsyncSession
) -> schemas.assets.Out:
    """
    Загрузить логотип для соцсети.
    
    Args:
        social: Провалидированный объект социальной сети
        s3_client: Клиент S3 для загрузки
        file: Файл изображения
        session: Сессия БД
        
    Returns:
        schemas.assets.Out: Информация о загруженном ассете
    """
    file_name: str = config.S3_ICON_TEMPLATE.format(
        card_id=social.card_id, 
        social_id=social.id
    )
    
    asset: models.CardAsset = await repo.logos.add(
        card_id=social.card_id, 
        social_id=social.id, 
        file_name=file_name, 
        session=session
    )
    
    await s3_client.upload_file(file.file, file_name)
    
    return schemas.assets.Out.model_validate(asset, from_attributes=True)

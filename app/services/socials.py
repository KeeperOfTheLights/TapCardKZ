"""
Сервис для работы с социальными сетями.

Содержит бизнес-логику создания и удаления социальных сетей.
"""
# Third-party
from sqlalchemy.ext.asyncio import AsyncSession

# Local
from app import repo, schemas
from app.core import config, models
from app.s3 import S3Client


async def create(   
    *, 
    card: models.Card,
    social: schemas.socials.In,
    session: AsyncSession
) -> schemas.socials.Out:
    """
    Создать соцсеть для карточки.
    
    Args:
        card: Провалидированный объект карточки
        social: Данные социальной сети
        session: Сессия БД
        
    Returns:
        schemas.socials.Out: Созданная социальная сеть
    """
    card_social: models.CardSocial = await repo.socials.create(
        card=card, 
        social=social, 
        session=session
    )
    
    return schemas.socials.Out.model_validate(card_social, from_attributes=True)


async def delete(
    *,
    social: models.CardSocial,
    card: models.Card,
    session: AsyncSession,
    s3_client: S3Client
) -> None:
    """
    Удалить соцсеть и связанную иконку.
    
    Args:
        social: Провалидированный объект социальной сети
        card: Объект карточки
        session: Сессия БД
        s3_client: Клиент S3 для удаления иконки
    """
    await repo.socials.delete(
        card=card, 
        social_id=social.id, 
        session=session
    )
    
    if social.icon_asset_id:
        file_name: str = config.S3_ICON_TEMPLATE.format(
            card_id=card.id, 
            social_id=social.id
        )
        await s3_client.delete_asset(file_name=file_name)
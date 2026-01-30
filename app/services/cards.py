"""
Сервис для работы с карточками.

Содержит бизнес-логику создания, получения и обновления карточек.
"""
# Third-party
from sqlalchemy.ext.asyncio import AsyncSession

# Local
from app import repo, schemas, utils
from app.core import models
from app.s3 import S3Client


async def get(
    *,
    s3_client: S3Client, 
    card: models.Card, 
    session: AsyncSession
) -> schemas.cards.Out:
    """
    Получить карточку со всеми связанными данными.
    
    Args:
        s3_client: Клиент S3 для получения URL
        card: Объект карточки
        session: Сессия БД
        
    Returns:
        schemas.cards.Out: Карточка с соцсетями и аватаром
    """
    logos_dict: dict[int, str] = await repo.logos.get(
        card_id=card.id, 
        session=session
    )
    
    for social in card.socials:
        link: str | None = logos_dict.get(social.icon_asset_id)
        social.app_icon_link = await s3_client.get_object_url(link) if link else None

    avatar: models.CardAsset | None = await repo.avatars.get(
        card_id=card.id, 
        session=session
    )
    avatar_link = await s3_client.get_object_url(avatar.file_name) if avatar else None
    card.avatar_link = avatar_link
    
    return schemas.cards.Out.model_validate(card, from_attributes=True)


async def create(
    *, 
    card: schemas.cards.In, 
    session: AsyncSession
) -> schemas.cards.OnCreate:
    """
    Создать новую карточку с кодом.
    
    Args:
        card: Данные для создания карточки
        session: Сессия БД
        
    Returns:
        schemas.cards.OnCreate: Созданная карточка с кодом активации
    """
    new_card: models.Card = await repo.cards.add(
        card=models.Card(**card.model_dump()), 
        session=session
    )

    generated_code: str = utils.code.generate()
    hashed_code: str = utils.code.encode(generated_code)
    
    code: models.Code = models.Code(
        card_id=new_card.id,
        code_hash=hashed_code,
        is_active=True
    )
    await repo.codes.add(code=code, session=session)
    
    card_schema: schemas.cards.Base = schemas.cards.Base.model_validate(
        new_card, 
        from_attributes=True
    )
    
    return utils.utils.build_schema(
        schemas.cards.OnCreate, 
        card_schema, 
        avatar_link=None, 
        code=generated_code
    )


async def update(
    *,
    card: models.Card, 
    card_update: schemas.cards.Patch,
    session: AsyncSession
) -> schemas.cards.Base:
    """
    Обновить карточку.
    
    Args:
        card: Объект карточки для обновления
        card_update: Данные для обновления
        session: Сессия БД
        
    Returns:
        schemas.cards.Base: Обновлённая карточка
    """
    update_data = card_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        if hasattr(card, key):
            setattr(card, key, value)
    
    await session.commit()
    await session.refresh(card)
    
    return card
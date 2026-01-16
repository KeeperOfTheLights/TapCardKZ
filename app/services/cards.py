from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, schemas
from app.core import models
from app.s3 import S3Client
from app.utils import utils
from app.utils.code import generate_code

async def get(
    *,
    s3_client: S3Client, 
    card_id: int, 
    session: AsyncSession
) -> schemas.cards.Out:
    card: models.Card | None = await repo.cards.get(card_id=card_id, session=session)

    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    logos_dict: dict[int, str] = await repo.logos.get(card_id=card_id, session=session)
    
    for social in card.socials:
        link: str | None = logos_dict.get(social.icon_asset_id)
        if not link:
            social.app_icon_link = None
            continue
        social.app_icon_link = await s3_client.get_object_url(link)

    avatar: CardAsset | None = await repo.avatars.get(card_id=card_id, session=session)
    avatar_filename: str = avatar.file_name 
    card.avatar_link = await s3_client.get_object_url(avatar_filename)

    return schemas.cards.Out.model_validate(card, from_attributes=True)

async def create(
    *, 
    card: schemas.cards.In, 
    session: AsyncSession
) -> schemas.cards.OnCreate:

    # 1. Создаем карточку
    created_card: models.Card = await repo.cards.add(card=models.Card(**card.model_dump()), session=session)

    # 2. Создаем код
    edit_token: str = generate_code()
    code: models.Code = models.Code(
        card_id=created_card.id,
        code_hash=edit_token,
        is_active=True
    )
    created_code: models.Code = await repo.codes.add(code=code, session=session)
    
    
    card: models.Card = await repo.cards.get(card_id=created_card.id, session=session)    

    setattr(card, "avatar_link", None)
    setattr(card, "code", created_code.code_hash)

    return schemas.cards.OnCreate.model_validate(card, from_attributes=True)

async def update(
    *,
    card_id: int, 
    card_update: schemas.cards.Patch, # Переименовали входной аргумент
    session: AsyncSession
) -> schemas.cards.Out:
    
    # 1. Получаем объект из базы
    card: models.Card | None = await repo.cards.get(card_id=card_id, session=session)
    
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # 2. Превращаем схему обновления в словарь
    # Используйте model_dump(exclude_unset=True), чтобы обновлять только те поля, 
    # которые пользователь прислал в запросе
    update_data = card_update.model_dump(exclude_unset=True)
    
    # 3. Обновляем поля модели
    for field, value in update_data.items():
        if field == "socials": # Если есть вложенные поля, их нужно обрабатывать отдельно
            continue
        setattr(card, field, value)
    
    # 4. Сохраняем
    await session.commit()
    await session.refresh(card)
    
    # Не забываем про avatar_link, если он обязателен в CardOut
    setattr(card, "avatar_link", None) 
    
    return schemas.cards.Out.model_validate(card, from_attributes=True)
    
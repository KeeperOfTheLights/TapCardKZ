from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import repo, schemas
from app.core.models.card import Card
from app.core.models.code import Code
from app.s3.client import S3Client
from app.utils import utils
from app.utils.code import generate_code

async def get_card(
    *,
    s3_client: S3Client, 
    card_id: int, 
    session: AsyncSession
) -> schemas.cards.CardOut:
    card: Card | None = await repo.cards.get_card(card_id=card_id, session=session)

    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    logos_dict: dict[int, str] = await repo.assets.get_logos(card_id=card_id, session=session)
    
    for social in card.socials:
        link: str | None = logos_dict.get(social.icon_asset_id)
        if not link:
            social.app_icon_link = None
            continue
        social.app_icon_link = await s3_client.get_object_url(link)

    avatar: CardAsset | None = await repo.assets.get_avatar(card_id=card_id, session=session)
    avatar_filename: str = avatar.file_name 
    card.avatar_link = await s3_client.get_object_url(avatar_filename)

    return schemas.cards.CardOut.model_validate(card, from_attributes=True)

async def create_card(*, card: schemas.cards.CardIn, session: AsyncSession) -> schemas.cards.CardOutOnCreate:

    # 1. Создаем карточку
    created_card: Card = await repo.cards.add_card(card=Card(**card.model_dump()), session=session)

    # 2. Создаем код
    edit_token: str = generate_code()
    code: Code = Code(
        card_id=created_card.id,
        code_hash=edit_token,
        is_active=True
    )
    created_code: Code = await repo.codes.add_code(code=code, session=session)
    
    
    card: Card = await repo.cards.get_card(card_id=created_card.id, session=session)    

    setattr(card, "avatar_link", None)
    setattr(card, "code", created_code.code_hash)

    return schemas.cards.CardOutOnCreate.model_validate(card, from_attributes=True)

async def update_card(
    *,
    card_id: int, 
    card_update: schemas.cards.CardPatch, # Переименовали входной аргумент
    session: AsyncSession
) -> schemas.cards.CardOut:
    
    # 1. Получаем объект из базы
    card: Card | None = await repo.cards.get_card(card_id=card_id, session=session)
    
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
    
    return schemas.cards.CardOut.model_validate(card, from_attributes=True)
    
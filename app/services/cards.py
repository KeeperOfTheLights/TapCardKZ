from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models.card import Card
from app.core.models.code import Code
from app import schemas
from sqlalchemy import select
from fastapi import HTTPException
from app.services.assets import get_avatar, get_logos
from sqlalchemy.orm import selectinload
from app.utils import utils
from app.s3.client import S3Client
from app.utils.code import generate_code

async def get_card(s3_client: S3Client, card_id: int, session: AsyncSession) -> schemas.cards.CardOut:
    # Загружаем карту и соцсети (они отсортированы базой по CardSocial.order_id)
    query = (
        select(Card)
        .where(Card.id == card_id)
        .options(selectinload(Card.socials)) 
    )
    result = await session.execute(query)
    card = result.scalar_one_or_none()

    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    # Получаем словарь всех логотипов {id_картинки: ссылка}
    logos_dict: dict[int, str] = await get_logos(card_id, s3_client, session)
    
    for social in card.socials:
        link = logos_dict.get(social.icon_asset_id)

        setattr(social, "app_icon_link", link)
        

    
    # Если нужно аватарку:
    card.avatar_link = await get_avatar(card_id, s3_client, session)

    return schemas.cards.CardOut.model_validate(card, from_attributes=True)

async def create_card(payload: schemas.cards.CardIn, session: AsyncSession) -> schemas.cards.CardOutOnCreate:
    card = Card(**payload.model_dump())
    session.add(card)
    await session.flush()  # Get card.id without committing

    edit_token = generate_code()
    code = Code(
        card_id=card.id,
        code_hash=edit_token,
        is_active=True
    )
    session.add(code)

    await session.commit()
    
    
    stmt = (
        select(Card)
        .where(Card.id == card.id)
        .options(selectinload(Card.socials))
    )
    res = await session.execute(stmt)

    card: Card = res.scalar_one()

    setattr(card, "avatar_link", None)
    setattr(card, "code", edit_token)

    return schemas.cards.CardOutOnCreate.model_validate(card, from_attributes=True)

async def update_card(
    card_id: int, 
    card_update: schemas.cards.CardPatch, # Переименовали входной аргумент
    session: AsyncSession
) -> schemas.cards.CardOut:
    
    # 1. Получаем объект из базы
    stmt = (
        select(Card)
        .where(Card.id == card_id)
        .options(selectinload(Card.socials))
    )
    res = await session.execute(stmt)
    
    card: Card = res.scalar_one_or_none()
    
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
    
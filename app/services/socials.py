from app.core.models.social import CardSocial
from app.core.models.card import Card
from app import schemas, repo
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import update   
from app.core.models.asset import CardAsset

from sqlalchemy import select, delete 
from sqlalchemy.orm import selectinload 

async def create_social(   
    *, 
    card_id: int,
    social: schemas.socials.SocialIn,
    session: AsyncSession,
) -> schemas.socials.SocialOut:
    # 1. Загружаем карту сразу вместе с соцсетями
    card: Card | None = await repo.cards.get_card(card_id=card_id, session=session)
    
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card with id {card_id} not found"
        )
    
    # 2. Создаем объект (не передаем order_id, пусть ordering_list решит сам)
    card_social: CardSocial = CardSocial(**social.model_dump())
    
    # 3. Добавляем в список (БЕЗ await, это обычный метод списка)
    # Благодаря ordering_list, объекту автоматически назначится верный order_id
    card.socials.append(card_social)
    
    # 4. Сохраняем
    await session.commit()
    await session.refresh(card_social)
    
    return schemas.socials.SocialOut.model_validate(card_social, from_attributes=True)

async def delete_social(*, card_id: int, social_id: int, session: AsyncSession):
    # 1. Обязательно загружаем карточку вместе с её соцсетями
    card: Card | None = await repo.cards.get_card(card_id=card_id, session=session)
    
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")

    # 2. Ищем нужный объект в списке socials
    target_social = next((s for s in card.socials if s.id == social_id), None)
    await session.execute(delete(CardAsset).where(CardAsset.id == target_social.icon_asset_id))
    await session.commit()
    if target_social:
        # 3. Удаляем объект из списка
        # В этот момент ordering_list автоматически изменит order_id у остальных!
        card.socials.remove(target_social)
        
        # 4. Сохраняем изменения
        await session.commit()
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Social not found")
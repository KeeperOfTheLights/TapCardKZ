from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, schemas, utils
from app.core import models
from app.s3 import S3Client

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
        social.app_icon_link = await s3_client.get_object_url(link) if link else None

    avatar: CardAsset | None = await repo.avatars.get(card_id=card_id, session=session)
    if avatar:
        avatar_filename: str = avatar.file_name 
        avatar_link: str = await s3_client.get_object_url(avatar_filename)
    else:
        avatar_link: None= None

    card.avatar_link = avatar_link
    return schemas.cards.Out.model_validate(card, from_attributes=True)

async def create(
    *, 
    card: schemas.cards.In, 
    session: AsyncSession
) -> schemas.cards.OnCreate:

    # 1. Создаем карточку
    card: models.Card = await repo.cards.add(card=models.Card(**card.model_dump()), session=session)

    # 2. Создаем код
    generated_code: str = utils.code.generate()
    hashed_code: str = utils.code.encode(generated_code)
    code: models.Code = models.Code(
        card_id=card.id,
        code_hash=hashed_code,
        is_active=True
    )
    code: models.Code = await repo.codes.add(code=code, session=session)
    card_schema: schemas.cards.Base = schemas.cards.Base.model_validate(card, from_attributes=True)

    return utils.utils.build_schema(schemas.cards.OnCreate, card_schema, avatar_link=None, code=generated_code)

async def update(
    *,
    card_id: int, 
    card_update: schemas.cards.Patch,
    session: AsyncSession
) -> schemas.cards.Base:
    
    card = await repo.cards.get(card_id=card_id, session=session)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # model_dump(exclude_unset=True) — критически важно, чтобы не затереть данные в БД дефолтами
    update_data = card_update.model_dump(exclude_unset=True)
    
    # Чистое обновление атрибутов объекта
    for key, value in update_data.items():
        if hasattr(card, key):
            setattr(card, key, value)
    
    await session.commit()
    await session.refresh(card)

    # Вместо build_schema — используем конструктор схемы напрямую
    return card
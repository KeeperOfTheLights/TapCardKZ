"""
Card service.

Contains business logic for creating, getting and updating cards.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, schemas, utils
from app.core import models
from app.core.config import config
from app.s3.client import S3Client
from app.services import avatars, logos


async def get(
    s3_client: S3Client, 
    card: models.Card, 
    session: AsyncSession
) -> schemas.cards.Out:
    """
    Get card with all related data.
    
    Args:
        s3_client: S3 client for getting URLs
        card: Card object
        session: Database session
        
    Returns:
        schemas.cards.Out: Card with socials and avatar
    """
    logos_dict: dict[int, str] = await logos.get_all(card_id=card.id, s3_client=s3_client, session=session)

    avatar: CardAsset | None = await repo.avatars.get(card_id=card.id, session=session)
    avatar_link: str | None = await s3_client.get_object_url(avatar.file_name) if avatar else None
    for social in card.socials:
        social.app_icon_link = logos_dict.get(social.icon_asset_id)
    card.avatar_link = avatar_link

    return schemas.cards.Out.model_validate(card, from_attributes=True)

async def create(
    card: schemas.cards.In, 
    session: AsyncSession
) -> schemas.cards.OnCreate:
    """
    Create new card with code.
    
    Args:
        card: Data for creating card
        session: Database session
        
    Returns:
        schemas.cards.OnCreate: Created card with activation code
    """
    card: models.Card = await repo.cards.create(card=models.Card(**card.model_dump()), session=session)

    generated_code: str = utils.code.generate()
    hashed_code: str = utils.code.encode(generated_code)
    code: models.Code = models.Code(
        card_id=card.id,
        code_hash=hashed_code,
        is_active=True
    )
    code: models.Code = await repo.codes.create(code=code, session=session)
    card_schema: schemas.cards.Base = schemas.cards.Base.model_validate(card, from_attributes=True)

    return utils.utils.build_schema(schemas.cards.OnCreate, card_schema, avatar_link=None, code=generated_code)


async def update(
    card: models.Card, 
    card_update: schemas.cards.Patch, 
    session: AsyncSession
) -> schemas.cards.Base:
    """
    Update card.
    
    Args:
        card: Card object to update
        card_update: Update data
        session: Database session
        
    Returns:
        schemas.cards.Base: Updated card
    """
    updated_card: models.Card = await repo.cards.update(
        card=card, 
        card_update=card_update.model_dump(exclude_unset=True), 
        session=session
    )
    
    return schemas.cards.Base.model_validate(updated_card)

    
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
    avatar_link: str | None = await avatars.get(
        card_id=card.id,
        s3_client=s3_client,
        session=session
    )
    
    socials_icons: dict = await logos.get_all(
        card_id=card.id,
        s3_client=s3_client,
        session=session
    )
    
    socials: list[schemas.socials.Out] = [
        utils.utils.build_schema(
            schemas.socials.Out,
            social,
            app_icon_link=socials_icons.get(social.id)
        )
        for social in card.socials
    ]
    
    return utils.utils.build_schema(
        schemas.cards.Out,
        card,
        socials=socials,
        avatar_link=avatar_link
    )


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
    code: str = utils.code.generate(config.CODE_LEN)
    hashed_code: str = utils.code.encode(code)
    
    card_record: models.Card = await repo.cards.create(
        card=card, 
        session=session
    )
    
    await repo.codes.create(
        code=hashed_code, 
        card_id=card_record.id, 
        session=session
    )
    
    return utils.utils.build_schema(
        schemas.cards.OnCreate,
        card_record,
        socials=[],
        avatar_link=None,
        code=code
    )


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
        card_update=card_update, 
        session=session
    )
    
    return schemas.cards.Base.model_validate(updated_card)
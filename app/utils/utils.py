from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import models, config

async def image_validator(
    *, 
    card_id: int, 
    file: UploadFile, 
    session: AsyncSession,
    max_size: int = config.IMAGE_MAX_SIZE,
    allowed_types: list[str] = config.ALLOWED_IMAGE_TYPES
) -> None:
    if file.size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Too large file, it must be less than 5MB"
        )

    card: models.Card | None = await session.get(models.Card, card_id)
    if not card:
        raise HTTPException(    
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card with id {card_id} not found"
        )

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not allowed file type, allowed types: {', '.join(allowed_types)}"
        )


from app.core import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

async def add(
    *, 
    code: models.Code, 
    session: AsyncSession
) -> models.Code:
    session.add(code)
    await session.commit()
    await session.refresh(code)
    return code

async def get_active(
    *, 
    code: str, 
    session: AsyncSession
) -> models.Code | None:
    query = select(models.Code).where(
        models.Code.is_active == True,
        models.Code.code_hash == code
    )
    result = await session.execute(query)
    code_record = result.scalar_one_or_none()
    return code_record

async def deactivate(
    *, 
    card_id: int, 
    session: AsyncSession
) -> None:
    await session.execute(
        update(models.Code)
        .where(models.Code.card_id == card_id)
        .values(is_active=False)
    )
    await session.commit()
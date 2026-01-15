
from app.core.models.code import Code
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

async def add_code(*, code: Code, session: AsyncSession) -> Code:
    session.add(code)
    await session.commit()
    await session.refresh(code)
    return code

async def is_active_code(*, code: str, session: AsyncSession) -> Code | None:
    query = select(Code).where(
        Code.is_active == True,
        Code.code_hash == code
    )
    result = await session.execute(query)
    code_record = result.scalar_one_or_none()
    return code_record

async def deactivate_codes(*, card_id: int, session: AsyncSession) -> None:
    await session.execute(
        update(Code)
        .where(Code.card_id == card_id)
        .values(is_active=False)
    )
    await session.commit()
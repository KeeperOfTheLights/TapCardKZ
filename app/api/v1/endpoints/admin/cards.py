from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_session, verify_admin
from app import schemas, services

router: APIRouter = APIRouter(prefix="/cards")

@router.post("/", response_model=schemas.cards.OnCreate)
async def create_card(
    card: schemas.cards.In,
    session: AsyncSession = Depends(get_session),
    #admin: dict = Depends(verify_admin)
) -> schemas.cards.OnCreate:
    return await services.cards.create(card=card, session=session)

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_session, verify_admin
from app import schemas, services

router: APIRouter = APIRouter(prefix="/cards")

@router.post("/", response_model=schemas.cards.CardOutOnCreate)
async def create_card(
    request: Request,
    card: schemas.cards.CardIn,
    session: AsyncSession = Depends(get_session),
    #admin: dict = Depends(verify_admin)
) -> schemas.cards.CardOutOnCreate:
    return await services.cards.create_card(card=card, session=session)

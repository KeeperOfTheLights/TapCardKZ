from fastapi import APIRouter, Depends, Request, Path

from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.services import cards
from app.api.v1.dependencies import get_session, verify_access_token

router = APIRouter(prefix="/cards")


@router.get("/{id}", response_model=schemas.cards.CardOut)
async def get_card(
    request: Request,
    id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session)
) -> schemas.cards.CardOut:
    return await cards.get_card(request.app.state.s3_client, id, session)

#FOR ADMIN
@router.post("/", response_model=schemas.cards.CardOutOnCreate)
async def create_card(
    request: Request,
    card: schemas.cards.CardIn,
    session: AsyncSession = Depends(get_session)
) -> schemas.cards.CardOutOnCreate:
    return await cards.create_card(card, session)

@router.patch("/{id}", response_model=schemas.cards.CardOut)
async def update_card(
    request: Request,
    card: schemas.cards.CardPatch,
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.cards.CardOut:
    return await cards.update_card(token["card_id"], card, session)



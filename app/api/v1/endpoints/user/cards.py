from fastapi import APIRouter, Depends, Request, Path

from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services
from app.api.v1.dependencies import get_session, verify_access_token

router: APIRouter = APIRouter(prefix="/cards")

@router.get("/{id}/", response_model=schemas.cards.Out)
async def get_card(
    request: Request,
    id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session)
) -> schemas.cards.Out:
    return await services.cards.get(
        card_id=id,
        s3_client=request.app.state.s3_client,
        session=session
    )

@router.patch("/{id}/", response_model=schemas.cards.Out)
async def update_card(
    request: Request,
    card: schemas.cards.Patch,
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.cards.Out:
    return await services.cards.update(
        card_id=token["card_id"],
        card_update=card,
        session=session
    )



from fastapi import APIRouter, Depends, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services, validators
from app.api.v1.dependencies import get_session, verify_access_token

router: APIRouter = APIRouter(prefix="/cards")

@router.get(
    "/me/", 
    response_model=schemas.cards.Out,
    summary="Get my card",
    description="Returns full card information including social links and avatar.",
)
async def get_me(
    request: Request,
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.cards.Out:
    """
    Get my card.
    """
    card = await validators.cards.require_card(card_id=token["card_id"], session=session)
    
    return await services.cards.get(
        card=card,
        s3_client=request.app.state.s3_client,
        session=session
    )

@router.get(
    "/{id}/", 
    response_model=schemas.cards.Out,
    summary="Get card",
    description="Returns full card information including social links and avatar.",
    responses={
        404: {"description": "Card not found"}
    }
)
async def get_card(
    request: Request,
    id: int = Path(..., ge=1, description="Card ID"),
    session: AsyncSession = Depends(get_session)
) -> schemas.cards.Out:
    """
    Get card by ID.
    
    - **id**: unique card identifier
    """
    card = await validators.cards.require_card(card_id=id, session=session)
    
    return await services.cards.get(
        card=card,
        s3_client=request.app.state.s3_client,
        session=session
    )


@router.patch(
    "/{id}/", 
    response_model=schemas.cards.Base,
    summary="Update card",
    description="Partial card update. Requires authorization.",
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Invalid token"},
        404: {"description": "Card not found"}
    }
)
async def update_card(
    request: Request,
    card: schemas.cards.Patch,
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.cards.Base:
    """
    Update card (PATCH).
    
    Pass only fields you want to change.
    Authorization via cookie: Authorization.
    """
    card_obj = await validators.cards.require_card(
        card_id=token["card_id"], 
        session=session
    )
    
    return await services.cards.update(
        card=card_obj,
        card_update=card,
        session=session
    )

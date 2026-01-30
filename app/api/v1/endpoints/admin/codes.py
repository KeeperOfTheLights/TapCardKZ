from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services, validators
from app.api.v1.dependencies import get_session, verify_admin

router: APIRouter = APIRouter(prefix="/codes")


@router.post(
    "/regenerate/", 
    response_model=schemas.codes.RegenerateOut,
    summary="Regenerate code",
    description="Deactivates current code and creates a new one. Admin only.",
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "Card not found"}
    }
)
async def regenerate_code(
    code: schemas.codes.RegenerateIn,
    session: AsyncSession = Depends(get_session),
    admin: dict = Depends(verify_admin)
) -> schemas.codes.RegenerateOut:
    """
    Regenerate activation code for a card.
    
    - **card_id**: Card ID to regenerate code for
    
    Old code will be deactivated, new code returned in response.
    """
    card = await validators.cards.require_card(
        card_id=code.card_id, 
        session=session
    )
    
    return await services.codes.regenerate(card=card, session=session)
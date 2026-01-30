from fastapi import APIRouter, Depends, Path, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services, validators
from app.api.v1.dependencies import get_session, verify_access_token

router: APIRouter = APIRouter(prefix="/socials")


@router.post(
    "/", 
    response_model=schemas.socials.Out,
    summary="Add social link",
    description="Adds new social link to card. Requires authorization.",
    responses={
        401: {"description": "Not authenticated"},
        404: {"description": "Card not found"}
    }
)
async def create_social(
    social: schemas.socials.In,
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(verify_access_token)
) -> schemas.socials.Out:
    """
    Add social link.
    
    - **type**: social network type (telegram, instagram, etc.)
    - **url**: profile URL
    - **label**: display text
    """
    card = await validators.cards.require_card(
        card_id=token["card_id"], 
        session=session
    )
    
    return await services.socials.create(
        card=card, 
        social=social, 
        session=session
    )


@router.delete(
    "/{social_id}/", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete social link",
    description="Deletes social link and associated icon. Requires authorization.",
    responses={
        401: {"description": "Not authenticated"},
        404: {"description": "Social link not found"}
    }
)
async def delete_social(
    request: Request,
    social_id: int = Path(..., ge=1, description="Social link ID"),
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(verify_access_token)
):
    """
    Delete social link.
    
    - **social_id**: ID of social link to delete
    
    Also deletes associated icon from S3.
    """
    card = await validators.cards.require_card(
        card_id=token["card_id"], 
        session=session
    )
    social = await validators.socials.require_social(
        card_id=token["card_id"], 
        social_id=social_id, 
        session=session
    )
    
    return await services.socials.delete(
        social=social,
        card=card, 
        session=session, 
        s3_client=request.app.state.s3_client
    )

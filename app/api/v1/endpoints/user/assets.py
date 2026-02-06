from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services, validators
from app.api.v1.dependencies import get_session, verify_access_token
from app.core import models
from app.s3.client import S3Client

router: APIRouter = APIRouter(prefix="/assets")


@router.post(
    "/avatar/", 
    response_model=schemas.assets.Out,
    summary="Upload avatar",
    description="Uploads or updates card avatar. "
                "Supported formats: JPEG, PNG. Max size: 5MB.",
    responses={
        400: {"description": "Invalid file type"},
        401: {"description": "Not authenticated"},
        404: {"description": "Card not found"},
        413: {"description": "File too large"}
    }
)
async def upload_avatar(
    request: Request, 
    file: UploadFile = File(..., description="Image file (JPEG, PNG)"),
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.assets.Out:
    """
    Upload avatar for card.
    
    - **file**: image in JPEG or PNG format
    
    Overwrites existing avatar if present.
    """
    await validators.assets.validate_image(file)
    
    card = await validators.cards.require_card(
        card_id=token["card_id"], 
        session=session
    )
    
    s3_client: S3Client = request.app.state.s3_client
    
    return await services.avatars.upload(
        card=card, 
        s3_client=s3_client, 
        file=file, 
        session=session
    )


@router.post(
    "/logo/", 
    response_model=schemas.assets.Out,
    summary="Upload social icon",
    description="Uploads custom icon for social link. "
                "Social link must not have an existing icon.",
    responses={
        400: {"description": "Invalid file type or icon already exists"},
        401: {"description": "Not authenticated"},
        404: {"description": "Social link not found"},
        413: {"description": "File too large"}
    }
)
async def upload_logo(
    request: Request, 
    social_id: int = Form(..., ge=1, description="Social link ID"),
    file: UploadFile = File(..., description="Image file (JPEG, PNG)"),
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.assets.Out:
    """
    Upload custom icon for social link.
    
    - **social_id**: social link ID
    - **file**: image in JPEG or PNG format
    
    Cannot upload icon if one already exists.
    """
    await validators.assets.validate_image(file)
    
    social: models.CardSocial = await validators.socials.require_social(
        card_id=token["card_id"], 
        social_id=social_id, 
        session=session
    )
    validators.socials.require_no_icon(social)
    
    s3_client: S3Client = request.app.state.s3_client
    
    return await services.logos.upload(
        social=social, 
        s3_client=s3_client, 
        file=file, 
        session=session
    )
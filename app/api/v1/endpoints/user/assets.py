from fastapi import APIRouter, Depends, File, UploadFile, Request, Form

from sqlalchemy.ext.asyncio import AsyncSession

from app import services, schemas
from app.api.v1.dependencies import get_session, verify_access_token
from app.s3.client import S3Client

router: APIRouter = APIRouter(prefix="/assets")

@router.post("/avatar/", response_model=schemas.assets.AssetOut)
async def upload_avatar(
    request: Request, 
    file: UploadFile = File(...),
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.assets.AssetOut:
    s3_client: S3Client = request.app.state.s3_client
    return await services.assets.upload_avatar(
        card_id=token["card_id"], 
        s3_client=s3_client, 
        file=file, 
        session=session
    )

@router.post("/logo/", response_model=schemas.assets.AssetOut)
async def upload_logo(
    request: Request, 
    social_id: int = Form(...),
    file: UploadFile = File(...),
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.assets.AssetOut:
    s3_client: S3Client = request.app.state.s3_client
    return await services.assets.upload_logo(
        card_id=token["card_id"], 
        social_id=social_id, 
        s3_client=s3_client, 
        file=file, 
        session=session
    )
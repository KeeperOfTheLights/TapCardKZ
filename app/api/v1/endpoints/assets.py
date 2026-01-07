from fastapi import APIRouter, Depends
from fastapi import File, UploadFile
from fastapi import Request
from fastapi import status
from app import services
from fastapi import HTTPException
from fastapi import Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.dependencies import get_session
from app.core.models.asset import CardAsset
from app.core.models.card import Card
from app import schemas
from fastapi import Form
from app.core.models.asset import AssetType
from app.s3.client import S3Client
from app.api.v1.dependencies import verify_access_token

router = APIRouter()

@router.post("/assets/avatar", response_model=schemas.assets.AssetOut)
async def upload_avatar(
    request: Request, 
    file: UploadFile = File(...),
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.assets.AssetOut:
    s3_client: S3Client = request.app.state.s3_client
    return await services.assets.upload_avatar(token["card_id"], s3_client, file, session)


@router.post("/assets/logo", response_model=schemas.assets.AssetOut)
async def upload_logo(
    request: Request, 
    social_id: int = Form(...),
    file: UploadFile = File(...),
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.assets.AssetOut:
    s3_client: S3Client = request.app.state.s3_client
    return await services.assets.upload_logo(token["card_id"], social_id, s3_client, file, session)
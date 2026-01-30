from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services, validators
from app.api.v1.dependencies import get_session, verify_access_token
from app.s3.client import S3Client

router: APIRouter = APIRouter(prefix="/assets")


@router.post(
    "/avatar/", 
    response_model=schemas.assets.Out,
    summary="Загрузить аватар",
    description="Загружает или обновляет аватар карточки. "
                "Поддерживаемые форматы: JPEG, PNG. Максимальный размер: 5MB.",
    responses={
        400: {"description": "Недопустимый тип файла"},
        401: {"description": "Не авторизован"},
        404: {"description": "Карточка не найдена"},
        413: {"description": "Файл слишком большой"}
    }
)
async def upload_avatar(
    request: Request, 
    file: UploadFile = File(..., description="Файл изображения (JPEG, PNG)"),
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.assets.Out:
    """
    Загрузить аватар для карточки.
    
    - **file**: изображение в формате JPEG или PNG
    
    Перезаписывает существующий аватар, если он есть.
    """
    validators.assets.validate_image(file)
    
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
    summary="Загрузить иконку соцсети",
    description="Загружает кастомную иконку для социальной сети. "
                "У соцсети не должно быть существующей иконки.",
    responses={
        400: {"description": "Недопустимый тип файла или иконка уже существует"},
        401: {"description": "Не авторизован"},
        404: {"description": "Социальная сеть не найдена"},
        413: {"description": "Файл слишком большой"}
    }
)
async def upload_logo(
    request: Request, 
    social_id: int = Form(..., ge=1, description="ID социальной сети"),
    file: UploadFile = File(..., description="Файл изображения (JPEG, PNG)"),
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.assets.Out:
    """
    Загрузить кастомную иконку для социальной сети.
    
    - **social_id**: ID социальной сети
    - **file**: изображение в формате JPEG или PNG
    
    Нельзя загрузить иконку, если она уже существует.
    """
    validators.assets.validate_image(file)
    
    social = await validators.socials.require_social(
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
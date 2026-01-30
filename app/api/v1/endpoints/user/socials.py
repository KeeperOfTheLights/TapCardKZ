from fastapi import APIRouter, Depends, Path, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services, validators
from app.api.v1.dependencies import get_session, verify_access_token

router: APIRouter = APIRouter(prefix="/socials")


@router.post(
    "/", 
    response_model=schemas.socials.Out,
    summary="Добавить социальную сеть",
    description="Добавляет новую социальную сеть к карточке. Требуется авторизация.",
    responses={
        401: {"description": "Не авторизован"},
        404: {"description": "Карточка не найдена"}
    }
)
async def create_social(
    social: schemas.socials.In,
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(verify_access_token)
) -> schemas.socials.Out:
    """
    Добавить социальную сеть.
    
    - **type**: тип социальной сети (telegram, instagram, etc.)
    - **url**: ссылка на профиль
    - **label**: отображаемый текст
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
    summary="Удалить социальную сеть",
    description="Удаляет социальную сеть и связанную иконку. Требуется авторизация.",
    responses={
        401: {"description": "Не авторизован"},
        404: {"description": "Социальная сеть не найдена"}
    }
)
async def delete_social(
    request: Request,
    social_id: int = Path(..., ge=1, description="ID социальной сети"),
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(verify_access_token)
):
    """
    Удалить социальную сеть.
    
    - **social_id**: ID социальной сети для удаления
    
    Также удаляет привязанную иконку из S3.
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

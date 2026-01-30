from fastapi import APIRouter, Depends, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, services, validators
from app.api.v1.dependencies import get_session, verify_access_token

router: APIRouter = APIRouter(prefix="/cards")


@router.get(
    "/{id}/", 
    response_model=schemas.cards.Out,
    summary="Получить карточку",
    description="Возвращает полную информацию о карточке, включая социальные сети и аватар.",
    responses={
        404: {"description": "Карточка не найдена"}
    }
)
async def get_card(
    request: Request,
    id: int = Path(..., ge=1, description="ID карточки"),
    session: AsyncSession = Depends(get_session)
) -> schemas.cards.Out:
    """
    Получить карточку по ID.
    
    - **id**: уникальный идентификатор карточки
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
    summary="Обновить карточку",
    description="Частичное обновление данных карточки. Требуется авторизация.",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Недействительный токен"},
        404: {"description": "Карточка не найдена"}
    }
)
async def update_card(
    request: Request,
    card: schemas.cards.Patch,
    token: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(get_session)
) -> schemas.cards.Base:
    """
    Обновить карточку (PATCH).
    
    Передайте только те поля, которые хотите изменить.
    Авторизация через cookie: Authorization.
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

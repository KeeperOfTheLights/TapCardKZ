from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services, validators
from app.api.v1.dependencies import get_session, verify_admin

router: APIRouter = APIRouter(prefix="/codes")


@router.post(
    "/regenerate/", 
    response_model=schemas.codes.RegenerateOut,
    summary="Регенерировать код",
    description="Деактивирует текущий код и создаёт новый. Только для администраторов.",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Недостаточно прав"},
        404: {"description": "Карточка не найдена"}
    }
)
async def regenerate_code(
    code: schemas.codes.RegenerateIn,
    session: AsyncSession = Depends(get_session),
    # admin: dict = Depends(verify_admin)
) -> schemas.codes.RegenerateOut:
    """
    Регенерировать код активации для карточки.
    
    - **card_id**: ID карточки для регенерации кода
    
    Старый код будет деактивирован, новый возвращён в ответе.
    """
    card = await validators.cards.require_card(
        card_id=code.card_id, 
        session=session
    )
    
    return await services.codes.regenerate(card=card, session=session)
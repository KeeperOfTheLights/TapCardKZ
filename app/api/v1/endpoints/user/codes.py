from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services, utils, validators
from app.api.v1.dependencies import get_session

router: APIRouter = APIRouter(prefix="/codes")


@router.post(
    "/redeem/", 
    response_model=schemas.codes.Out,
    summary="Активировать код",
    description="Проверяет код и возвращает JWT токен для редактирования карточки. "
                "Токен устанавливается в cookie 'Authorization'.",
    responses={
        401: {"description": "Неверный код или код не найден"}
    }
)
async def redeem_code(
    code: schemas.codes.In,
    response: Response,
    session: AsyncSession = Depends(get_session)
) -> schemas.codes.Out:
    """
    Активировать код и получить токен.
    
    - **code**: код активации, полученный при создании карточки
    
    После успешной активации токен устанавливается в cookie.
    """
    hashed_code: str = utils.code.encode(code.code)
    
    code_record = await validators.codes.require_active_code(
        code_hash=hashed_code, 
        session=session
    )
    
    return await services.codes.redeem(
        code_record=code_record, 
        response=response
    )

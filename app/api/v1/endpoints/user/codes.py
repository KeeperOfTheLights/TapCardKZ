from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services, utils, validators
from app.api.v1.dependencies import get_session

router: APIRouter = APIRouter(prefix="/codes")


@router.post(
    "/redeem/", 
    response_model=schemas.codes.Out,
    summary="Redeem code",
    description="Validates code and returns JWT token for card editing. "
                "Token is set in 'Authorization' cookie.",
    responses={
        401: {"description": "Invalid code or code not found"}
    }
)
async def redeem_code(
    code: schemas.codes.In,
    response: Response,
    session: AsyncSession = Depends(get_session)
) -> schemas.codes.Out:
    """
    Redeem code and get token.
    
    - **code**: activation code received when creating card
    
    After successful redemption, token is set in cookie.
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

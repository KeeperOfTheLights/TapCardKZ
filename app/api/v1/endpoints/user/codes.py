from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services, utils, validators
from app.api.v1.dependencies import get_session, verify_access_token

router: APIRouter = APIRouter(prefix="/codes")


@router.post(
    "/redeem/", 
    response_model=schemas.codes.Out,
    summary="Redeem code",
    description="Validates code and returns JWT token for card editing. "
                "Token is set in 'Authorization' cookie. "
                "If valid token already exists in cookies, it will be reused.",
    responses={
        401: {"description": "Invalid code or code not found"}
    }
)
async def redeem_code(
    code: schemas.codes.In,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session)
) -> schemas.codes.Out:
    """
    Redeem code and get token.
    
    - **code**: activation code received when creating card
    
    After successful redemption, token is set in cookie.
    If valid token already exists for this card, it will be reused.
    """
    hashed_code: str = utils.code.encode(code.code)
    
    code_record = await validators.codes.require_active_code(
        code_hash=hashed_code, 
        session=session
    )
    
    return await services.codes.redeem(
        code_record=code_record,
        request=request, 
        response=response
    )


@router.get(
    "/verify-token/",
    summary="Verify current token",
    description="Check if the current token in cookies is valid",
    responses={
        200: {"description": "Token is valid"},
        401: {"description": "Token is missing"},
        403: {"description": "Token is invalid"}
    }
)
async def verify_token(
    request: Request,
    payload: dict = Depends(verify_access_token)
):
    """
    Verify current token from cookies.
    
    Returns card_id if token is valid.
    """
    return {
        "valid": True,
        "card_id": payload.get("card_id"),
        "token_type": payload.get("type"),
        "expires_at": payload.get("exp")
    }

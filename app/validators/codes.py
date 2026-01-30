"""
Activation code validators.

Check code existence and active status.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo
from app.core import models


async def require_active_code(code_hash: str, session: AsyncSession) -> models.Code:
    """
    Verify active code existence.
    
    Args:
        code_hash: Code hash to check
        session: Database session
        
    Returns:
        models.Code: Found active code
        
    Raises:
        HTTPException: 401 if code not found or inactive
    """
    code: models.Code | None = await repo.codes.get_active(
        code=code_hash, 
        session=session
    )
    if not code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid code or code not found"
        )
    return code

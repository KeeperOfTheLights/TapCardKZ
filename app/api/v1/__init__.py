from fastapi import APIRouter, Request, Depends, HTTPException, status

from app.api.v1.endpoints.admin import router as admin_router
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.dependencies import verify_admin

router: APIRouter = APIRouter(prefix="/v1")

router.include_router(admin_router, dependencies=[Depends(verify_admin)])
router.include_router(user_router)
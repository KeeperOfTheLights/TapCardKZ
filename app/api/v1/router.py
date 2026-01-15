from fastapi import APIRouter

from app.api.v1.endpoints.admin import router as admin_router
from app.api.v1.endpoints.user import router as user_router

router: APIRouter = APIRouter(prefix="/v1")

router.include_router(admin_router)
router.include_router(user_router)
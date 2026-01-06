from fastapi import APIRouter

from app.api.v1.endpoints.cards import router as cards_router
from app.api.v1.endpoints.codes import router as codes_router

router = APIRouter(prefix="/v1")

router.include_router(cards_router)
router.include_router(codes_router)
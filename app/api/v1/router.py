from fastapi import APIRouter

from app.api.v1.endpoints.cards import router as cards_router

router = APIRouter(prefix="/v1")

router.include_router(cards_router)
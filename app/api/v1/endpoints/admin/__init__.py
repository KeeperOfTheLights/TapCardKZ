from fastapi import APIRouter

from .cards import router as cards_router
from .codes import router as codes_router

router: APIRouter = APIRouter(tags=["Admin"])

router.include_router(cards_router)
router.include_router(codes_router)
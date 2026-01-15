from fastapi import APIRouter

from .cards import router as cards_router
from .codes import router as codes_router
from .socials import router as socials_router
from .assets import router as assets_router

router: APIRouter = APIRouter(tags=["User"])

router.include_router(cards_router)
router.include_router(codes_router)
router.include_router(socials_router)
router.include_router(assets_router)
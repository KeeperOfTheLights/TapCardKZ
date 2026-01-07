from fastapi import APIRouter

from app.api.v1.endpoints.cards import router as cards_router
from app.api.v1.endpoints.assets import router as assets_router
from app.api.v1.endpoints.socials import router as socials_router
from app.api.v1.endpoints.codes import router as codes_router

router: APIRouter = APIRouter(prefix="/v1")

router.include_router(cards_router)
router.include_router(assets_router)
router.include_router(socials_router)
router.include_router(codes_router)
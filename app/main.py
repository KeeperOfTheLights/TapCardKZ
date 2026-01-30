import sys
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.lifespan import lifespan
from app.api.v1 import router as v1_router


from fastapi.staticfiles import StaticFiles


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api", lifespan=lifespan)
    
    app.mount("/admin", StaticFiles(directory="app/static/admin", html=True), name="admin")

    app.include_router(v1_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

app: FastAPI = create_app()

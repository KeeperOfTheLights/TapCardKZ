from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.lifespan import lifespan
from app.api.v1 import router as v1_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api", lifespan=lifespan)
    
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

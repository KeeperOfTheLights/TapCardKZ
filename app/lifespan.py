from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.app_state.setup_db import setup_db, cleanup_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    print("App starting...")
    await setup_db(app)
    yield
    # shutdown
    print("App shutting down...")
    await cleanup_db(app)
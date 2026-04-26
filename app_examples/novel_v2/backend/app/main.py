from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api.routes import stories, game, auth
from app.models.session import Base
from sqlalchemy.ext.asyncio import create_async_engine
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s"
)

settings = get_settings()

app = FastAPI(
    title="Novel V2 API", description="Visual Novel Game API", version="1.0.0"
)


@app.on_event("startup")
async def startup():
    # Create database tables
    engine = create_async_engine(settings.database_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stories.router, prefix="/api")
app.include_router(game.router, prefix="/api")
app.include_router(auth.router, prefix="/api")


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}


# Media file serving
from fastapi.staticfiles import StaticFiles
from pathlib import Path

stories_path = Path(settings.stories_dir)
if stories_path.exists():
    app.mount("/api/media", StaticFiles(directory=str(stories_path)), name="media")

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import get_settings
from app.repositories.session_repository import SessionRepository
from app.services.game_service import GameService
from app.adapters.postgres_game_engine import PostgresGameEngine
from app.adapters.disk_scene_adapter import DiskSceneAdapter
from app.adapters.disk_story_reader import DiskStoryReader

settings = get_settings()

engine = create_async_engine(settings.database_url, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


def get_session_repository(db: AsyncSession = Depends(get_db)) -> SessionRepository:
    return SessionRepository(db)


def get_game_service(
    repo: SessionRepository = Depends(get_session_repository),
) -> GameService:
    # These would be singleton instances in production
    scene_adapter = DiskSceneAdapter(settings.stories_dir)
    story_reader = DiskStoryReader(settings.stories_dir, settings.media_base_url)
    engine = PostgresGameEngine(repo, scene_adapter, story_reader)
    return GameService(engine, scene_adapter, story_reader)

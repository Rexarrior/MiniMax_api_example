from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import get_settings
from app.repositories.session_repository import SessionRepository
from app.services.game_service import GameService
from app.adapters.postgres_game_engine import PostgresGameEngine
from app.adapters.disk_scene_adapter import DiskSceneAdapter
from app.adapters.disk_story_reader import DiskStoryReader
from functools import lru_cache

settings = get_settings()

# Lazy initialization of database engine
_engine = None
_async_session_maker = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(settings.database_url, echo=False)
    return _engine


def _get_session_maker():
    global _async_session_maker
    if _async_session_maker is None:
        _async_session_maker = async_sessionmaker(_get_engine(), expire_on_commit=False)
    return _async_session_maker


async def get_db() -> AsyncSession:
    async with _get_session_maker()() as session:
        yield session


def get_session_repository(db: AsyncSession = Depends(get_db)) -> SessionRepository:
    return SessionRepository(db)


# Singleton instances for adapters
_scene_adapter = None
_story_reader = None
_game_engine = None


def _get_scene_adapter() -> DiskSceneAdapter:
    global _scene_adapter
    if _scene_adapter is None:
        _scene_adapter = DiskSceneAdapter(settings.stories_dir)
    return _scene_adapter


def _get_story_reader() -> DiskStoryReader:
    global _story_reader
    if _story_reader is None:
        _story_reader = DiskStoryReader(settings.stories_dir, settings.media_base_url)
    return _story_reader


def _get_game_engine(repo: SessionRepository) -> PostgresGameEngine:
    global _game_engine
    if _game_engine is None:
        _game_engine = PostgresGameEngine(
            repo,
            _get_scene_adapter(),
            _get_story_reader()
        )
    return _game_engine


def get_game_service(
    repo: SessionRepository = Depends(get_session_repository),
) -> GameService:
    # Use singleton instances
    engine = _get_game_engine(repo)
    return GameService(engine, _get_scene_adapter(), _get_story_reader())

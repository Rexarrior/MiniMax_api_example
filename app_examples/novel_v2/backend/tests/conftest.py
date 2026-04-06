import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.session import Base, GameSessionModel


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_db():
    """Create an in-memory SQLite database for testing"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_maker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session_maker() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def sample_session_data():
    """Sample session data for testing"""
    return {
        "user_id": "test_user",
        "story_id": "demo",
        "current_scene_id": "intro",
        "dialogue_index": 0,
        "is_ending": False,
        "choices_json": [
            {"text": "Choice 1", "next": "scene1"},
            {"text": "Choice 2", "next": "scene2"},
        ],
        "dialogues_json": [
            {
                "speaker": "narrator",
                "text": "Hello world",
                "mood": None,
                "voice_url": None,
                "character_image_url": None,
            },
            {
                "speaker": "hero",
                "text": "How are you?",
                "mood": "happy",
                "voice_url": None,
                "character_image_url": None,
            },
        ],
    }

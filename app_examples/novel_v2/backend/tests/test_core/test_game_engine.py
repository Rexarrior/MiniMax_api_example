import pytest
from app.core.game_engine import GameEngine, GameSession
from app.core.exceptions import SessionNotFoundError, InvalidChoiceError


class MockGameEngine(GameEngine):
    """Mock implementation for testing"""

    def __init__(self):
        self.sessions = {}

    async def start_session(
        self, story_id: str, user_id: str | None = None
    ) -> GameSession:
        session = GameSession(
            session_id="test-session-123",
            user_id=user_id,
            story_id=story_id,
            current_scene_id="intro",
            dialogue_index=0,
            is_ending=False,
            background_url=None,
            music_url=None,
            current_character_image_url=None,
            choices=[],
            dialogues=[],
            created_at=None,
            updated_at=None,
        )
        self.sessions[session.session_id] = session
        return session

    async def get_session(self, session_id: str) -> GameSession | None:
        return self.sessions.get(session_id)

    async def make_choice(self, session_id: str, choice_index: int) -> GameSession:
        session = self.sessions.get(session_id)
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")
        if choice_index < 0 or choice_index >= len(session.choices):
            raise InvalidChoiceError(f"Invalid choice index: {choice_index}")
        return session

    async def advance_dialogue(self, session_id: str) -> GameSession:
        session = self.sessions.get(session_id)
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")
        session.dialogue_index += 1
        return session


class TestGameEngine:
    @pytest.fixture
    def engine(self):
        return MockGameEngine()

    @pytest.mark.asyncio
    async def test_start_session(self, engine):
        session = await engine.start_session("demo", "user123")

        assert session.story_id == "demo"
        assert session.user_id == "user123"
        assert session.current_scene_id == "intro"
        assert session.dialogue_index == 0
        assert session.is_ending is False

    @pytest.mark.asyncio
    async def test_get_session(self, engine):
        created = await engine.start_session("demo")
        retrieved = await engine.get_session(created.session_id)

        assert retrieved is not None
        assert retrieved.session_id == created.session_id

    @pytest.mark.asyncio
    async def test_get_nonexistent_session(self, engine):
        result = await engine.get_session("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_make_choice_invalid_index(self, engine):
        await engine.start_session("demo")

        with pytest.raises(InvalidChoiceError):
            await engine.make_choice("test-session-123", 999)

    @pytest.mark.asyncio
    async def test_advance_dialogue(self, engine):
        await engine.start_session("demo")
        session = await engine.advance_dialogue("test-session-123")

        assert session.dialogue_index == 1

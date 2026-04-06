import pytest
from datetime import datetime
from uuid import uuid4

from app.models.session import GameSessionModel
from app.repositories.session_repository import SessionRepository


class TestSessionRepository:
    @pytest.mark.asyncio
    async def test_create_session(self, test_db, sample_session_data):
        repo = SessionRepository(test_db)

        model = GameSessionModel(
            user_id=sample_session_data["user_id"],
            story_id=sample_session_data["story_id"],
            current_scene_id=sample_session_data["current_scene_id"],
            dialogue_index=sample_session_data["dialogue_index"],
            is_ending=sample_session_data["is_ending"],
            choices_json=sample_session_data["choices_json"],
            dialogues_json=sample_session_data["dialogues_json"],
        )

        created = await repo.create(model)

        assert created.session_id is not None
        assert created.story_id == "demo"

    @pytest.mark.asyncio
    async def test_get_session(self, test_db, sample_session_data):
        repo = SessionRepository(test_db)

        model = GameSessionModel(
            user_id=sample_session_data["user_id"],
            story_id=sample_session_data["story_id"],
            current_scene_id=sample_session_data["current_scene_id"],
            dialogue_index=sample_session_data["dialogue_index"],
            is_ending=sample_session_data["is_ending"],
            choices_json=sample_session_data["choices_json"],
            dialogues_json=sample_session_data["dialogues_json"],
        )

        created = await repo.create(model)
        retrieved = await repo.get(str(created.session_id))

        assert retrieved is not None
        assert str(retrieved.session_id) == str(created.session_id)

    @pytest.mark.asyncio
    async def test_update_session(self, test_db, sample_session_data):
        repo = SessionRepository(test_db)

        model = GameSessionModel(
            user_id=sample_session_data["user_id"],
            story_id=sample_session_data["story_id"],
            current_scene_id=sample_session_data["current_scene_id"],
            dialogue_index=sample_session_data["dialogue_index"],
            is_ending=sample_session_data["is_ending"],
            choices_json=sample_session_data["choices_json"],
            dialogues_json=sample_session_data["dialogues_json"],
        )

        created = await repo.create(model)
        created.dialogue_index = 5
        updated = await repo.update(created)

        assert updated.dialogue_index == 5

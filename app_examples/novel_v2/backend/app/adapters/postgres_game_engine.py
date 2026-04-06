from app.core.game_engine import GameEngine, GameSession
from app.core.scene_adapter import SceneAdapter, SceneData
from app.core.story_reader import StoryReader
from app.core.exceptions import (
    SessionNotFoundError,
    SceneNotFoundError,
    InvalidChoiceError,
)
from app.models.session import GameSessionModel
from app.repositories.session_repository import SessionRepository
from datetime import datetime
from typing import Optional


class PostgresGameEngine(GameEngine):
    def __init__(
        self,
        session_repo: SessionRepository,
        scene_adapter: SceneAdapter,
        story_reader: StoryReader,
    ):
        self.session_repo = session_repo
        self.scene_adapter = scene_adapter
        self.story_reader = story_reader

    async def _resolve_scene_assets(
        self, scene_data: SceneData, story_id: str
    ) -> tuple[Optional[str], Optional[str], Optional[str]]:
        background_url = None
        if scene_data.background:
            background_url = await self.story_reader.get_background_url(
                story_id, scene_data.background
            )

        music_url = None
        if scene_data.music:
            music_url = await self.story_reader.get_audio_url(
                story_id, scene_data.music
            )

        current_character_image_url = None
        if scene_data.dialogues:
            first_dialogue = scene_data.dialogues[0]
            if first_dialogue.character_image_url:
                current_character_image_url = await self.story_reader.get_image_url(
                    story_id, first_dialogue.character_image_url
                )

        return (background_url, music_url, current_character_image_url)

    async def start_session(
        self, story_id: str, user_id: str | None = None
    ) -> GameSession:
        start_scene_id = await self.scene_adapter.get_story_start_scene(story_id)
        scene_data = await self.scene_adapter.load_scene(story_id, start_scene_id)

        (
            background_url,
            music_url,
            current_character_image_url,
        ) = await self._resolve_scene_assets(scene_data, story_id)

        session_model = GameSessionModel(
            user_id=user_id,
            story_id=story_id,
            current_scene_id=start_scene_id,
            dialogue_index=0,
            is_ending=False,
            background_url=background_url,
            music_url=music_url,
            current_character_image_url=current_character_image_url,
            choices_json=[
                {"text": c.text, "next": c.next_scene_id} for c in scene_data.choices
            ],
            dialogues_json=[
                {
                    "speaker": d.speaker,
                    "text": d.text,
                    "mood": d.mood,
                    "voice_url": d.voice_url,
                    "character_image_url": d.character_image_url,
                }
                for d in scene_data.dialogues
            ],
            next_scene_id=scene_data.next_scene_id,
        )

        created = await self.session_repo.create(session_model)
        return self._model_to_session(created)

    async def get_session(self, session_id: str) -> GameSession | None:
        model = await self.session_repo.get(session_id)
        if not model:
            return None
        return self._model_to_session(model)

    async def make_choice(self, session_id: str, choice_index: int) -> GameSession:
        model = await self.session_repo.get(session_id)
        if not model:
            raise SessionNotFoundError(f"Session {session_id} not found")

        choices = model.choices_json
        if choice_index < 0 or choice_index >= len(choices):
            raise InvalidChoiceError(f"Invalid choice index: {choice_index}")

        next_scene_id = choices[choice_index]["next"]

        scene_data = await self.scene_adapter.load_scene(model.story_id, next_scene_id)

        (
            background_url,
            music_url,
            current_character_image_url,
        ) = await self._resolve_scene_assets(scene_data, model.story_id)

        model.current_scene_id = next_scene_id
        model.dialogue_index = 0
        model.is_ending = scene_data.is_ending
        model.background_url = background_url
        model.music_url = music_url
        model.current_character_image_url = current_character_image_url
        model.choices_json = [
            {"text": c.text, "next": c.next_scene_id} for c in scene_data.choices
        ]
        model.dialogues_json = [
            {
                "speaker": d.speaker,
                "text": d.text,
                "mood": d.mood,
                "voice_url": d.voice_url,
                "character_image_url": d.character_image_url,
            }
            for d in scene_data.dialogues
        ]
        model.next_scene_id = scene_data.next_scene_id
        model.updated_at = datetime.utcnow()

        updated = await self.session_repo.update(model)
        return self._model_to_session(updated)

    async def advance_dialogue(self, session_id: str) -> GameSession:
        model = await self.session_repo.get(session_id)
        if not model:
            raise SessionNotFoundError(f"Session {session_id} not found")

        model.dialogue_index += 1

        if model.dialogue_index >= len(model.dialogues_json):
            if model.next_scene_id:
                scene_data = await self.scene_adapter.load_scene(
                    model.story_id, model.next_scene_id
                )
                (
                    background_url,
                    music_url,
                    current_character_image_url,
                ) = await self._resolve_scene_assets(scene_data, model.story_id)

                model.current_scene_id = model.next_scene_id
                model.dialogue_index = 0
                model.is_ending = scene_data.is_ending
                model.background_url = background_url
                model.music_url = music_url
                model.current_character_image_url = current_character_image_url
                model.choices_json = [
                    {"text": c.text, "next": c.next_scene_id}
                    for c in scene_data.choices
                ]
                model.dialogues_json = [
                    {
                        "speaker": d.speaker,
                        "text": d.text,
                        "mood": d.mood,
                        "voice_url": d.voice_url,
                        "character_image_url": d.character_image_url,
                    }
                    for d in scene_data.dialogues
                ]
                model.next_scene_id = scene_data.next_scene_id
            elif not model.choices_json:
                model.is_ending = True

        model.updated_at = datetime.utcnow()
        updated = await self.session_repo.update(model)
        return self._model_to_session(updated)

    def _model_to_session(self, model: GameSessionModel) -> GameSession:
        return GameSession(
            session_id=str(model.session_id),
            user_id=model.user_id,
            story_id=model.story_id,
            current_scene_id=model.current_scene_id,
            dialogue_index=model.dialogue_index,
            is_ending=model.is_ending,
            background_url=model.background_url,
            music_url=model.music_url,
            current_character_image_url=model.current_character_image_url,
            choices=model.choices_json,
            dialogues=model.dialogues_json,
            next_scene_id=model.next_scene_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

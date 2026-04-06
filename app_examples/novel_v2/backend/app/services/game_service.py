from app.core.game_engine import GameEngine
from app.core.scene_adapter import SceneAdapter, StoryMetadata
from app.core.story_reader import StoryReader
from app.core.exceptions import (
    SessionNotFoundError,
    SceneNotFoundError,
    InvalidChoiceError,
)
from app.schemas.session import SessionResponse, SessionCreate
from app.schemas.scene import SceneResponse, ChoiceRequest, DialogueSchema, ChoiceSchema
from typing import Optional
import time


class GameService:
    def __init__(
        self, engine: GameEngine, scene_adapter: SceneAdapter, story_reader: StoryReader
    ):
        self.engine = engine
        self.scene_adapter = scene_adapter
        self.story_reader = story_reader

    async def list_stories(self) -> list[StoryMetadata]:
        return await self.scene_adapter.list_stories()

    async def start_game(self, request: SessionCreate) -> SessionResponse:
        session = await self.engine.start_session(request.story_id, request.user_id)
        return self._session_to_response(session)

    async def get_session(self, session_id: str) -> SessionResponse:
        session = await self.engine.get_session(session_id)
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")
        return self._session_to_response(session)

    async def get_scene(self, session_id: str) -> SceneResponse:
        session = await self.engine.get_session(session_id)
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")

        scene_data = await self.scene_adapter.load_scene(
            session.story_id, session.current_scene_id
        )

        # Build full scene response with URLs
        background_url = None
        if scene_data.background:
            background_url = await self.story_reader.get_background_url(
                session.story_id, scene_data.background
            )

        music_url = None
        if scene_data.music:
            music_url = await self.story_reader.get_audio_url(
                session.story_id, scene_data.music
            )

        # Get current character image based on dialogue
        current_char_image = None
        if session.dialogue_index < len(scene_data.dialogues):
            dialogue = scene_data.dialogues[session.dialogue_index]
            if dialogue.character_image_url:
                current_char_image = await self.story_reader.get_image_url(
                    session.story_id, dialogue.character_image_url
                )

        dialogues = []
        for d in scene_data.dialogues:
            # Resolve voice_url if present
            voice_url = None
            if d.voice_url:
                voice_url = await self.story_reader.get_voice_url(
                    session.story_id, d.speaker, d.voice_url
                )
            # Resolve character_image_url if present (it's a filename, not path)
            char_image_url = None
            if d.character_image_url:
                char_image_url = await self.story_reader.get_image_url(
                    session.story_id, d.character_image_url
                )
            dialogues.append(
                DialogueSchema(
                    speaker=d.speaker,
                    text=d.text,
                    mood=d.mood,
                    voice_url=voice_url,
                    character_image_url=char_image_url,
                )
            )

        choices = [
            ChoiceSchema(text=c.text, next_scene_id=c.next_scene_id)
            for c in scene_data.choices
        ]

        return SceneResponse(
            scene_id=scene_data.id,
            title=scene_data.title,
            background_url=background_url,
            background_video_url=None,
            dialogues=dialogues,
            choices=choices,
            is_ending=scene_data.is_ending,
            music_url=music_url,
            current_character_image_url=current_char_image,
            timestamp=int(time.time() * 1000),
        )

    async def make_choice(
        self, session_id: str, request: ChoiceRequest
    ) -> SessionResponse:
        session = await self.engine.make_choice(session_id, request.choice_index)
        return self._session_to_response(session)

    async def advance_dialogue(self, session_id: str) -> SessionResponse:
        session = await self.engine.advance_dialogue(session_id)
        return self._session_to_response(session)

    def _session_to_response(self, session) -> SessionResponse:
        return SessionResponse(
            session_id=str(session.session_id),
            user_id=session.user_id,
            story_id=session.story_id,
            current_scene_id=session.current_scene_id,
            dialogue_index=session.dialogue_index,
            is_ending=session.is_ending,
            background_url=session.background_url,
            music_url=session.music_url,
            current_character_image_url=session.current_character_image_url,
            choices=session.choices,
            dialogues=session.dialogues,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

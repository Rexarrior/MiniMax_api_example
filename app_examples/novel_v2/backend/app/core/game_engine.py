from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class GameSession:
    session_id: str
    user_id: Optional[str]
    story_id: str
    language: str
    current_scene_id: str
    dialogue_index: int
    is_ending: bool
    background_url: Optional[str]
    music_url: Optional[str]
    current_character_image_url: Optional[str]
    choices: list[dict]
    dialogues: list[dict]
    created_at: datetime
    updated_at: datetime
    next_scene_id: Optional[str] = None


class GameEngine(ABC):
    @abstractmethod
    async def start_session(
        self, story_id: str, user_id: str | None = None, language: str = "en"
    ) -> GameSession:
        """Start a new game session"""
        pass

    @abstractmethod
    async def get_session(self, session_id: str) -> GameSession | None:
        """Get session by ID"""
        pass

    @abstractmethod
    async def make_choice(self, session_id: str, choice_index: int) -> GameSession:
        """Make a choice and advance to next scene"""
        pass

    @abstractmethod
    async def advance_dialogue(self, session_id: str) -> GameSession:
        """Advance to next dialogue in current scene"""
        pass

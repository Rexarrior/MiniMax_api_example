from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Character:
    id: str
    name: str
    default_mood: str
    description: str


@dataclass
class DialogueLine:
    speaker: str
    text: str
    mood: Optional[str] = None
    voice_url: Optional[str] = None
    character_image_url: Optional[str] = None


@dataclass
class Choice:
    text: str
    next_scene_id: str


@dataclass
class SceneData:
    id: str
    title: str
    background: Optional[str]
    music: Optional[str]
    dialogues: list[DialogueLine]
    choices: list[Choice]
    is_ending: bool = False
    next_scene_id: Optional[str] = None


@dataclass
class StoryMetadata:
    id: str
    title: str
    author: str
    description: str
    version: str


class SceneAdapter(ABC):
    @abstractmethod
    async def load_scene(self, story_id: str, scene_id: str) -> SceneData:
        """Load a specific scene from a story"""
        pass

    @abstractmethod
    async def list_stories(self) -> list[StoryMetadata]:
        """List all available stories"""
        pass

    @abstractmethod
    async def get_characters(self, story_id: str) -> dict[str, Character]:
        """Get all characters in a story"""
        pass

    @abstractmethod
    async def get_story_start_scene(self, story_id: str) -> str:
        """Get the starting scene ID for a story"""
        pass

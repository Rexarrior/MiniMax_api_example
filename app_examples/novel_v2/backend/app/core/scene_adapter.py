from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Union


# Type alias for multilingual text: either a simple string (backward compat) or dict of lang->text
MultilangText = Union[str, dict[str, str]]


def get_text(text: MultilangText, language: str = "en") -> str:
    """Extract text in the requested language from a multilingual text field.

    Args:
        text: Either a plain string (backward compat) or dict {lang: text}
        language: Preferred language code (default: "en")

    Returns:
        Text in requested language, or English if not available, or original string
    """
    if isinstance(text, str):
        return text
    if isinstance(text, dict):
        if language in text:
            return text[language]
        if "en" in text:
            return text["en"]
        # Return first available language
        return next(iter(text.values()), "")
    return str(text)


@dataclass
class Character:
    id: str
    name: str
    default_mood: str
    description: str


@dataclass
class DialogueLine:
    speaker: str
    text: MultilangText  # Supports multilingual: str or dict[lang, str]
    mood: Optional[str] = None
    voice_url: Optional[str] = None
    character_image_url: Optional[str] = None

    def get_text(self, language: str = "en") -> str:
        """Get dialogue text in the specified language."""
        return get_text(self.text, language)


@dataclass
class Choice:
    text: MultilangText  # Supports multilingual: str or dict[lang, str]
    next_scene_id: str

    def get_text(self, language: str = "en") -> str:
        """Get choice text in the specified language."""
        return get_text(self.text, language)


@dataclass
class SceneData:
    id: str
    title: MultilangText  # Supports multilingual
    background: Optional[str]
    music: Optional[str]
    dialogues: list[DialogueLine]
    choices: list[Choice]
    is_ending: bool = False
    next_scene_id: Optional[str] = None

    def get_title(self, language: str = "en") -> str:
        """Get scene title in the specified language."""
        return get_text(self.title, language)


@dataclass
class StoryMetadata:
    id: str
    title: str
    author: str
    description: str
    version: str


class SceneAdapter(ABC):
    @abstractmethod
    async def load_scene(self, story_id: str, scene_id: str, language: str = "en") -> SceneData:
        """Load a specific scene from a story

        Args:
            story_id: The story identifier
            scene_id: The scene identifier
            language: Language code for multilingual content (default: "en")
        """
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

"""Scene parser for visual novel."""

from __future__ import annotations

import logging
import yaml
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class DialogueLine:
    speaker: str
    text: str
    mood: str | None = None
    image_prompt: str | None = None


@dataclass
class Choice:
    text: str
    next_scene: str


@dataclass
class Scene:
    id: str
    title: str
    background: str | None = None
    background_prompt: str | None = None
    dialogues: list[DialogueLine] = field(default_factory=list)
    choices: list[Choice] = field(default_factory=list)
    generate_image: str | None = None
    generate_music: str | None = None
    music: str | None = None
    next_scene: str | None = None
    is_video: bool = False
    video_prompt: str | None = None
    video_duration: int = 6


def parse_scene(scene_id: str, content: str) -> Scene:
    try:
        data = yaml.safe_load(content) or {}
    except yaml.YAMLError as e:
        logger.error(f"Failed to parse YAML for scene {scene_id}: {e}")
        data = {}

    dialogues = []
    for d in data.get("dialogue", []):
        if "character" in d:
            speaker = d["character"]
            text = d.get("text", "")
            mood = d.get("mood")
            image_prompt = d.get("image_prompt")
        elif "narrator" in d:
            speaker = "narrator"
            text = d.get("narrator", "") or ""
            mood = None
            image_prompt = d.get("image_prompt")
        else:
            continue
        dialogues.append(
            DialogueLine(
                speaker=speaker, text=text, mood=mood, image_prompt=image_prompt
            )
        )

    choices = []
    for c in data.get("choice", []):
        choices.append(Choice(text=c.get("text", ""), next_scene=c.get("next", "")))

    return Scene(
        id=scene_id,
        title=data.get("title", scene_id),
        background=data.get("background"),
        background_prompt=data.get("background_prompt"),
        dialogues=dialogues,
        choices=choices,
        generate_image=data.get("generate_image"),
        generate_music=data.get("generate_music"),
        music=data.get("music"),
        next_scene=data.get("next"),
        is_video=data.get("is_video", False),
        video_prompt=data.get("video_prompt"),
        video_duration=data.get("video_duration", 6),
    )

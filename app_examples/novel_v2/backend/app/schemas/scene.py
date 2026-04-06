from pydantic import BaseModel
from typing import Optional


class DialogueSchema(BaseModel):
    speaker: str
    text: str
    mood: Optional[str] = None
    voice_url: Optional[str] = None
    character_image_url: Optional[str] = None


class ChoiceSchema(BaseModel):
    text: str
    next_scene_id: str


class SceneResponse(BaseModel):
    scene_id: str
    title: str
    background_url: Optional[str]
    background_video_url: Optional[str]
    dialogues: list[DialogueSchema]
    choices: list[ChoiceSchema]
    is_ending: bool
    music_url: Optional[str]
    current_character_image_url: Optional[str]
    timestamp: int


class ChoiceRequest(BaseModel):
    choice_index: int

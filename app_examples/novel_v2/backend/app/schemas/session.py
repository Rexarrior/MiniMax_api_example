from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SessionCreate(BaseModel):
    story_id: str
    user_id: Optional[str] = None


class SessionResponse(BaseModel):
    session_id: str
    user_id: Optional[str]
    story_id: str
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

    class Config:
        from_attributes = True

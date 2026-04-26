from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class GameSessionModel(Base):
    __tablename__ = "game_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=True, index=True)
    story_id = Column(String(255), nullable=False, index=True)
    language = Column(String(10), default="en")
    current_scene_id = Column(String(255), nullable=False)
    dialogue_index = Column(Integer, default=0)
    is_ending = Column(Boolean, default=False)
    background_url = Column(Text, nullable=True)
    music_url = Column(Text, nullable=True)
    current_character_image_url = Column(Text, nullable=True)
    choices_json = Column(JSON, default=list)
    dialogues_json = Column(JSON, default=list)
    next_scene_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "session_id": str(self.session_id),
            "user_id": self.user_id,
            "story_id": self.story_id,
            "current_scene_id": self.current_scene_id,
            "dialogue_index": self.dialogue_index,
            "is_ending": self.is_ending,
            "background_url": self.background_url,
            "music_url": self.music_url,
            "current_character_image_url": self.current_character_image_url,
            "choices": self.choices_json,
            "dialogues": self.dialogues_json,
            "next_scene_id": self.next_scene_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

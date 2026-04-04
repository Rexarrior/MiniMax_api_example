"""Database models for session persistence."""

import os
import threading
import time
from typing import Any

from sqlalchemy import Column, String, Boolean, Float, Text, create_engine
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base()


class GameSession(Base):
    __tablename__ = "game_sessions"

    session_id = Column(String(255), primary_key=True)
    story_id = Column(String(255), nullable=True)
    story_path = Column(String(512), nullable=True)
    scene_id = Column(String(255), default="")
    title = Column(String(512), default="")
    choices = Column(JSON, default=list)
    is_ending = Column(Boolean, default=False)
    background_url = Column(String(1024), nullable=True)
    music_url = Column(String(1024), nullable=True)
    dialogues = Column(JSON, default=list)
    current_character_image_url = Column(String(1024), nullable=True)
    last_update = Column(Float, default=0)
    pending_choice = Column(String(10), nullable=True)
    pending_choice_time = Column(Float, default=0)
    created_at = Column(Float, default=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "title": self.title,
            "background_url": self.background_url,
            "dialogues": self.dialogues or [],
            "choices": self.choices or [],
            "is_ending": self.is_ending,
            "music_url": self.music_url,
            "timestamp": self.last_update,
            "current_character_image_url": self.current_character_image_url,
            "story_id": self.story_id,
        }


class Database:
    _instance = None
    _lock = threading.Lock()

    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(bind=self.engine)

    @classmethod
    def get_instance(cls, database_url: str = None) -> "Database":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    if database_url is None:
                        database_url = os.environ.get(
                            "DATABASE_URL",
                            "postgresql://novel:novel@localhost:5432/novel",
                        )
                    cls._instance = cls(database_url)
        return cls._instance

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

    def close(self):
        if self.engine:
            self.engine.dispose()

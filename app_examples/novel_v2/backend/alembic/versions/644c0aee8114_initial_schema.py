"""initial schema - create game_sessions table

Revision ID: 644c0aee8114
Revises:
Create Date: 2026-04-05 20:27:36.188790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


# revision identifiers, used by Alembic.
revision: str = '644c0aee8114'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create game_sessions table."""
    op.create_table(
        'game_sessions',
        sa.Column('session_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', sa.String(255), nullable=True),
        sa.Column('story_id', sa.String(255), nullable=False),
        sa.Column('language', sa.String(10), server_default='en', nullable=False),
        sa.Column('current_scene_id', sa.String(255), nullable=False),
        sa.Column('dialogue_index', sa.Integer, server_default='0', nullable=False),
        sa.Column('is_ending', sa.Boolean, server_default='false', nullable=False),
        sa.Column('background_url', sa.Text, nullable=True),
        sa.Column('music_url', sa.Text, nullable=True),
        sa.Column('current_character_image_url', sa.Text, nullable=True),
        sa.Column('choices_json', JSON, server_default='[]', nullable=False),
        sa.Column('dialogues_json', JSON, server_default='[]', nullable=False),
        sa.Column('next_scene_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # Create indexes
    op.create_index('ix_game_sessions_user_id', 'game_sessions', ['user_id'])
    op.create_index('ix_game_sessions_story_id', 'game_sessions', ['story_id'])


def downgrade() -> None:
    """Drop game_sessions table."""
    op.drop_index('ix_game_sessions_story_id', table_name='game_sessions')
    op.drop_index('ix_game_sessions_user_id', table_name='game_sessions')
    op.drop_table('game_sessions')

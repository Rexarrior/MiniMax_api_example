from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID
from app.models.session import GameSessionModel


class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, session: GameSessionModel) -> GameSessionModel:
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get(self, session_id: str) -> Optional[GameSessionModel]:
        result = await self.db.execute(
            select(GameSessionModel).where(
                GameSessionModel.session_id == UUID(session_id)
            )
        )
        return result.scalar_one_or_none()

    async def update(self, session: GameSessionModel) -> GameSessionModel:
        await self.db.commit()
        await self.db.refresh(session)
        return session

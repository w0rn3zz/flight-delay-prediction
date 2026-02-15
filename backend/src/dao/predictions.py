import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Prediction


class PredictionDAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, prediction: Prediction) -> Prediction:
        self.session.add(prediction)
        await self.session.commit()
        await self.session.refresh(prediction)
        return prediction

    async def get_by_id(self, prediction_id: uuid.UUID) -> Prediction | None:
        result = await self.session.execute(
            select(Prediction).where(Prediction.id == prediction_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Prediction]:
        result = await self.session.execute(
            select(Prediction)
            .order_by(Prediction.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(select(func.count(Prediction.id)))
        return result.scalar_one()

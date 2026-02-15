import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    month: Mapped[int] = mapped_column(Integer)
    day_of_month: Mapped[int] = mapped_column(Integer)
    day_of_week: Mapped[int] = mapped_column(Integer)
    dep_time: Mapped[int] = mapped_column(Integer)
    carrier: Mapped[str] = mapped_column(String(3))
    origin: Mapped[str] = mapped_column(String(4))
    dest: Mapped[str] = mapped_column(String(4))
    distance: Mapped[int] = mapped_column(Integer)

    model_name: Mapped[str] = mapped_column(String(50))
    predicted_delayed: Mapped[bool] = mapped_column(Boolean)
    delay_probability: Mapped[float] = mapped_column(Float)

    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class FlightPredictionRequestSchema(BaseModel):
    month: int = Field(..., ge=1, le=12)
    day_of_month: int = Field(..., ge=1, le=31)
    day_of_week: int = Field(..., ge=1, le=7)
    dep_time: int = Field(..., ge=0, le=2359)
    carrier: str = Field(..., min_length=2, max_length=3)
    origin: str = Field(..., min_length=3, max_length=4)
    dest: str = Field(..., min_length=3, max_length=4)
    distance: int = Field(..., ge=0)


class FlightPredictionResponseSchema(BaseModel):
    prediction_id: uuid.UUID
    delayed: bool
    delay_probability: float
    no_delay_probability: float
    model_used: str
    created_at: datetime

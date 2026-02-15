import time
import uuid
from datetime import datetime, timezone

from src.agents.base import BaseMLAgent
from src.core.schemas.predictions import FlightPredictionRequestSchema, FlightPredictionResponseSchema
from src.dao.predictions import PredictionDAO
from src.core.models import Prediction


class PredictionService:
    def __init__(self, agents: dict[str, BaseMLAgent], dao: PredictionDAO) -> None:
        self.agents = agents
        self.dao = dao

    async def predict(
        self, request: FlightPredictionRequestSchema, model_name: str
    ) -> FlightPredictionResponseSchema:
        agent = self.agents.get(model_name)
        if agent is None:
            available = list(self.agents.keys())
            raise ValueError(f"Model '{model_name}' not found. Available: {available}")

        if not agent.is_loaded():
            raise RuntimeError(f"Model '{model_name}' is not loaded")

        data = request.model_dump()

        start = time.perf_counter()
        result = agent.predict(data)
        latency_ms = int((time.perf_counter() - start) * 1000)

        prediction = Prediction(
            id=uuid.uuid4(),
            created_at=datetime.now(timezone.utc),
            month=request.month,
            day_of_month=request.day_of_month,
            day_of_week=request.day_of_week,
            dep_time=request.dep_time,
            carrier=request.carrier,
            origin=request.origin,
            dest=request.dest,
            distance=request.distance,
            model_name=model_name,
            predicted_delayed=result["delayed"],
            delay_probability=result["delay_probability"],
            latency_ms=latency_ms,
        )

        saved = await self.dao.create(prediction)

        return FlightPredictionResponseSchema(
            prediction_id=saved.id,
            delayed=saved.predicted_delayed,
            delay_probability=saved.delay_probability,
            no_delay_probability=1.0 - saved.delay_probability,
            model_used=saved.model_name,
            created_at=saved.created_at,
        )

    async def get_prediction(
        self, prediction_id: uuid.UUID
    ) -> FlightPredictionResponseSchema | None:
        p = await self.dao.get_by_id(prediction_id)
        if p is None:
            return None
        return self._to_response(p)

    async def get_history(
        self, limit: int = 100, offset: int = 0
    ) -> tuple[list[FlightPredictionResponseSchema], int]:
        predictions = await self.dao.get_all(limit=limit, offset=offset)
        total = await self.dao.count()
        return [self._to_response(p) for p in predictions], total

    def available_models(self) -> list[str]:
        return [name for name, agent in self.agents.items() if agent.is_loaded()]

    @staticmethod
    def _to_response(p: Prediction) -> FlightPredictionResponseSchema:
        return FlightPredictionResponseSchema(
            prediction_id=p.id,
            delayed=p.predicted_delayed,
            delay_probability=p.delay_probability,
            no_delay_probability=1.0 - p.delay_probability,
            model_used=p.model_name,
            created_at=p.created_at,
        )

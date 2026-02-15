import uuid

from fastapi import APIRouter, HTTPException, Query

from src.api.dependencies import PredictionServiceDep
from src.core.enums import AgentNameEnum
from src.core.schemas.predictions import FlightPredictionRequestSchema, FlightPredictionResponseSchema

router = APIRouter()


@router.post("/", response_model=FlightPredictionResponseSchema)
async def create_prediction(
    request: FlightPredictionRequestSchema,
    service: PredictionServiceDep,
    model_name: AgentNameEnum = Query(default=AgentNameEnum.CATBOOST_DEFAULT),
):
    return await service.predict(request, model_name.value)


@router.get("/", response_model=list[FlightPredictionResponseSchema])
async def list_predictions(
    service: PredictionServiceDep,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    predictions, _ = await service.get_history(limit=limit, offset=offset)
    return predictions


@router.get("/{prediction_id}", response_model=FlightPredictionResponseSchema)
async def get_prediction(
    prediction_id: uuid.UUID,
    service: PredictionServiceDep,
):
    result = await service.get_prediction(prediction_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return result

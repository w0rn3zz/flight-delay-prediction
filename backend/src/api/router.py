from fastapi import APIRouter

from src.api.dependencies import AgentsDep
from src.api.v1.predictions import router as predictions_router
from src.core.schemas.agents import ModelInfoSchema, StatusResponse

router = APIRouter(prefix="/api/v1")

router.include_router(predictions_router, prefix="/predictions", tags=["predictions"])


@router.get("/models", tags=["models"])
async def list_models(
    agents: AgentsDep,
) -> StatusResponse:
    models = [
        ModelInfoSchema(name=name, is_loaded=agent.is_loaded())
        for name, agent in agents.items()
    ]
    return StatusResponse(status="ok", models=models)

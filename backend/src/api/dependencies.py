from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.base import BaseMLAgent
from src.core.db_helper import db_helper
from src.dao.predictions import PredictionDAO
from src.services.predictions import PredictionService


# ── Session ──────────────────────────────────────────────────────────
SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]

# ── Agents ───────────────────────────────────────────────────────────
def get_agents(request: Request) -> dict[str, BaseMLAgent]:
    return request.app.state.agents


AgentsDep = Annotated[dict[str, BaseMLAgent], Depends(get_agents)]

# ── DAO ──────────────────────────────────────────────────────────────
def get_prediction_dao(session: SessionDep) -> PredictionDAO:
    return PredictionDAO(session)


PredictionDAODep = Annotated[PredictionDAO, Depends(get_prediction_dao)]

# ── Service ──────────────────────────────────────────────────────────
def get_prediction_service(
    dao: PredictionDAODep,
    agents: AgentsDep,
) -> PredictionService:
    return PredictionService(agents=agents, dao=dao)


PredictionServiceDep = Annotated[PredictionService, Depends(get_prediction_service)]

import logging

from src.agents import (
    CatBoostDefaultAgent,
    CatBoostOptimizedAgent,
    LightGBMDefaultAgent,
    LightGBMOptimizedAgent,
)

logger = logging.getLogger(__name__)

def agents_setup():
    agent_classes = {
        "catboost_default": CatBoostDefaultAgent,
        "catboost_optimized": CatBoostOptimizedAgent,
        "lightgbm_default": LightGBMDefaultAgent,
        "lightgbm_optimized": LightGBMOptimizedAgent,
    }

    agents = {}
    for name, cls in agent_classes.items():
        try:
            agents[name] = cls()
        except Exception as e:
            logger.warning(f"Could not load {name}: {e}")
    
    return agents
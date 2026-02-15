from enum import StrEnum


class AgentNameEnum(StrEnum):
    CATBOOST_DEFAULT = "catboost_default"
    CATBOOST_OPTIMIZED = "catboost_optimized"
    LIGHTGBM_DEFAULT = "lightgbm_default"
    LIGHTGBM_OPTIMIZED = "lightgbm_optimized"

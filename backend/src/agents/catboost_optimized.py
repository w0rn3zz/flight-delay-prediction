import pickle
from pathlib import Path
from typing import Any

import pandas as pd

from src.core.config import settings

from .base import BaseMLAgent


class CatBoostOptimizedAgent(BaseMLAgent):
    def __init__(self) -> None:
        super().__init__(settings.ml.catboost_optimized_path)

    def load(self, path: Path) -> Any:
        with open(path, "rb") as f:
            return pickle.load(f)

    def preprocess(self, data: dict[str, Any]) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "Month": data["month"],
                    "DayofMonth": data["day_of_month"],
                    "DayOfWeek": data["day_of_week"],
                    "DepTime": data["dep_time"],
                    "UniqueCarrier": data["carrier"],
                    "Origin": data["origin"],
                    "Dest": data["dest"],
                    "Distance": data["distance"],
                }
            ]
        )

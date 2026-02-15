import pickle
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from src.core.config import settings

from .base import BaseMLAgent


class LightGBMDefaultAgent(BaseMLAgent):
    def __init__(self) -> None:
        self.encoders: dict | None = None
        super().__init__(settings.ml.lightgbm_default_path)

    def load(self, path: Path) -> Any:
        model = joblib.load(path)
        encoders_path = Path(settings.ml.label_encoders_path)
        if encoders_path.exists():
            with open(encoders_path, "rb") as f:
                self.encoders = pickle.load(f)
        return model

    def preprocess(self, data: dict[str, Any]) -> np.ndarray:
        if self.encoders is None:
            raise RuntimeError("Label encoders not available for LightGBM")
        return np.array(
            [
                [
                    data["month"],
                    data["day_of_month"],
                    data["day_of_week"],
                    data["dep_time"],
                    self.encoders["UniqueCarrier"].transform([data["carrier"]])[0],
                    self.encoders["Origin"].transform([data["origin"]])[0],
                    self.encoders["Dest"].transform([data["dest"]])[0],
                    data["distance"],
                ]
            ]
        )

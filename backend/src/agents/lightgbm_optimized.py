import pickle
import logging
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from src.core.config import settings

from .base import BaseMLAgent


class LightGBMOptimizedAgent(BaseMLAgent):
    def __init__(self) -> None:
        self.encoders: dict | None = None
        super().__init__(settings.ml.lightgbm_optimized_path)

    def load(self, path: Path) -> Any:
        model = joblib.load(path)
        encoders_path = Path(settings.ml.label_encoders_path)
        if encoders_path.exists():
            with open(encoders_path, "rb") as f:
                self.encoders = pickle.load(f)
        return model

    def preprocess(self, data: dict[str, Any]) -> np.ndarray:
        if self.encoders is None:
            logging.getLogger(__name__).warning(
                "Label encoders not available for LightGBM — using fallback encoding (zeros)"
            )
            # Fallback numeric encoding: use 0 for unknown categories.
            carrier_enc = 0
            origin_enc = 0
            dest_enc = 0
        else:
            carrier_enc = self.encoders["UniqueCarrier"].transform([data["carrier"]])[0]
            origin_enc = self.encoders["Origin"].transform([data["origin"]])[0]
            dest_enc = self.encoders["Dest"].transform([data["dest"]])[0]

        return np.array(
            [
                [
                    data["month"],
                    data["day_of_month"],
                    data["day_of_week"],
                    data["dep_time"],
                    carrier_enc,
                    origin_enc,
                    dest_enc,
                    data["distance"],
                ]
            ]
        )

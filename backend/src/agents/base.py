import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class BaseMLAgent(ABC):
    def __init__(self, model_path: str) -> None:
        self.model_path = Path(model_path)
        self.model: Any = None
        self._is_loaded = False
        self._init_model()

    def _init_model(self) -> None:
        if not self.model_path.exists():
            logger.warning(f"Model file not found: {self.model_path}")
            return
        try:
            self.model = self.load(self.model_path)
            self._is_loaded = True
            logger.info(f"{self.name} loaded from {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load {self.name}: {e}")

    @abstractmethod
    def load(self, path: Path) -> Any: ...

    @abstractmethod
    def preprocess(self, data: dict[str, Any]) -> Any: ...

    def is_loaded(self) -> bool:
        return self._is_loaded and self.model is not None

    def predict(self, data: dict[str, Any]) -> dict[str, Any]:
        if not self.is_loaded():
            raise RuntimeError(f"{self.name} is not loaded")
        processed = self.preprocess(data)
        proba = self.model.predict_proba(processed)[0]
        return {
            "delayed": bool(proba[1] > 0.5),
            "delay_probability": float(proba[1]),
            "no_delay_probability": float(proba[0]),
        }

    @property
    def name(self) -> str:
        return self.__class__.__name__

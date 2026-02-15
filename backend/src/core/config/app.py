from .base import BaseConfig


class AppConfig(BaseConfig):
    title: str = "Flight Delay Prediction API"
    version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

from pydantic import BaseModel

from .app import AppConfig
from .database import DatabaseConfig
from .ml import MLConfig


class Settings(BaseModel):
    app: AppConfig = AppConfig()
    db: DatabaseConfig = DatabaseConfig()
    ml: MLConfig = MLConfig()


settings = Settings()

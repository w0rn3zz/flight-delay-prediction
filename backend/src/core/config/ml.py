from .base import BaseConfig


class MLConfig(BaseConfig):
    catboost_default_path: str = "ml/catboost_default_model.pkl"
    catboost_optimized_path: str = "ml/catboost_optimized_model.pkl"
    lightgbm_default_path: str = "ml/lightgbm_default_model.pkl"
    lightgbm_optimized_path: str = "ml/lightgbm_optimized_model.pkl"
    label_encoders_path: str = "ml/label_encoders.pkl"

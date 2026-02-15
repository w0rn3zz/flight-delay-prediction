from pydantic import BaseModel


class ModelInfoSchema(BaseModel):
    name: str
    is_loaded: bool


class StatusResponse(BaseModel):
    status: str
    models: list[ModelInfoSchema]


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None

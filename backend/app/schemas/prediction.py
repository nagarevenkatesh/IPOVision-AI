from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PredictionCreate(BaseModel):
    ipo_id: int


class PredictionResponse(BaseModel):
    id: int
    ipo_id: int
    predicted_return: float
    confidence_score: Optional[float] = None
    model_version: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
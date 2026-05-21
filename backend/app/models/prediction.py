from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ipo_id = Column(Integer, ForeignKey("ipos.id"), nullable=False)

    predicted_return = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=True)
    model_version = Column(String(50), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="predictions")
    ipo = relationship("IPO", back_populates="predictions")
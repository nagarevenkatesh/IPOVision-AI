from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class IPO(Base):
    __tablename__ = "ipos"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    ticker = Column(String(50), unique=True, index=True, nullable=False)
    sector = Column(String(100), nullable=True)
    exchange = Column(String(50), nullable=True)
    issue_price = Column(Float, nullable=False)
    listing_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    predictions = relationship("Prediction", back_populates="ipo")
from pydantic import BaseModel
from datetime import date
from typing import Optional


class IPOCreate(BaseModel):
    company_name: str
    ticker: str
    sector: Optional[str] = None
    exchange: Optional[str] = None
    issue_price: float
    listing_date: date


class IPOOut(BaseModel):
    id: int
    company_name: str
    ticker: str
    sector: Optional[str] = None
    exchange: Optional[str] = None
    issue_price: float
    listing_date: date

    class Config:
        from_attributes = True
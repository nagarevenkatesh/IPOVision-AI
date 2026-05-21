from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.ipo import IPO
from app.schemas.ipo import IPOCreate


def create_ipo(db: Session, ipo_in: IPOCreate) -> IPO:
    existing_ipo = db.query(IPO).filter(IPO.ticker == ipo_in.ticker).first()
    if existing_ipo:
        raise HTTPException(status_code=400, detail="IPO with this ticker already exists")

    new_ipo = IPO(
        company_name=ipo_in.company_name,
        ticker=ipo_in.ticker,
        sector=ipo_in.sector,
        exchange=ipo_in.exchange,
        issue_price=ipo_in.issue_price,
        listing_date=ipo_in.listing_date,
    )

    db.add(new_ipo)
    db.commit()
    db.refresh(new_ipo)
    return new_ipo


def get_all_ipos(db: Session):
    return db.query(IPO).order_by(IPO.listing_date.desc()).all()


def get_ipo_by_id(db: Session, ipo_id: int):
    ipo = db.query(IPO).filter(IPO.id == ipo_id).first()
    if not ipo:
        raise HTTPException(status_code=404, detail="IPO not found")
    return ipo
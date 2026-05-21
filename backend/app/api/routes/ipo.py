from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.ipo import IPO
from app.schemas.ipo import IPOCreate, IPOOut

router = APIRouter(prefix="/ipos", tags=["IPOs"])


@router.post("/", response_model=IPOOut, status_code=status.HTTP_201_CREATED)
def create_ipo(
    ipo_in: IPOCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    existing_ipo = db.query(IPO).filter(IPO.ticker == ipo_in.ticker).first()

    if existing_ipo:
        raise HTTPException(
            status_code=400,
            detail="IPO with this ticker already exists",
        )

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


@router.get("/", response_model=List[IPOOut])
def get_all_ipos(
    db: Session = Depends(get_db),
):
    ipos = db.query(IPO).all()
    return ipos


@router.get("/{ipo_id}", response_model=IPOOut)
def get_ipo(
    ipo_id: int,
    db: Session = Depends(get_db),
):
    ipo = db.query(IPO).filter(IPO.id == ipo_id).first()

    if not ipo:
        raise HTTPException(
            status_code=404,
            detail="IPO not found",
        )

    return ipo
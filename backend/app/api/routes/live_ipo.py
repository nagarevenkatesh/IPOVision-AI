from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.live_ipo_service import sync_live_ipos
from app.schemas.live_ipo import SyncResponse

router = APIRouter(prefix="/live-ipos", tags=["Live IPOs"])


@router.post("/sync", response_model=SyncResponse)
def sync_ipos(db: Session = Depends(get_db)):
    try:
        return sync_live_ipos(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
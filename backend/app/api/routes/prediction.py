from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.prediction import Prediction
from app.models.ipo import IPO
from app.schemas.prediction import PredictionCreate, PredictionResponse
from app.services.model_service import predict_listing_return

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post("/", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
def create_prediction(
    req: PredictionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    ipo = db.query(IPO).filter(IPO.id == req.ipo_id).first()
    if not ipo:
        raise HTTPException(status_code=404, detail="IPO not found")

    predicted_return, confidence = predict_listing_return(
        issue_price=ipo.issue_price,
        sector=ipo.sector or "",
        exchange=ipo.exchange or "",
    )

    new_prediction = Prediction(
        user_id=current_user.id,
        ipo_id=ipo.id,
        predicted_return=predicted_return,
        confidence_score=confidence,
        model_version="v1",
    )

    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return new_prediction


@router.get("/", response_model=list[PredictionResponse])
def get_my_predictions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    predictions = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )
    return predictions
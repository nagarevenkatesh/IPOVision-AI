from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.ipo import IPO
from app.models.prediction import Prediction
from app.utils.helpers import calculate_prediction_label

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def get_dashboard_data(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    total_ipos = db.query(func.count(IPO.id)).scalar() or 0

    total_predictions = (
        db.query(func.count(Prediction.id))
        .filter(Prediction.user_id == current_user.id)
        .scalar()
        or 0
    )

    latest_ipos = (
        db.query(IPO)
        .order_by(IPO.listing_date.desc())
        .limit(5)
        .all()
    )

    recent_predictions_rows = (
        db.query(Prediction, IPO.company_name)
        .join(IPO, Prediction.ipo_id == IPO.id)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .limit(5)
        .all()
    )

    recent_predictions = []
    for pred, company_name in recent_predictions_rows:
        recent_predictions.append({
            "id": pred.id,
            "ipo_id": pred.ipo_id,
            "company_name": company_name,
            "predicted_return": pred.predicted_return,
            "label": calculate_prediction_label(pred.predicted_return),
            "confidence_score": pred.confidence_score,
            "model_version": pred.model_version,
            "created_at": pred.created_at,
        })

    return {
        "total_ipos": total_ipos,
        "total_predictions": total_predictions,
        "latest_ipos": latest_ipos,
        "recent_predictions": recent_predictions,
    }
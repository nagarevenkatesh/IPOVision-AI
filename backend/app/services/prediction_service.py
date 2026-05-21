from sqlalchemy.orm import Session

from app.models.prediction import Prediction
from app.models.ipo import IPO
from app.services.model_service import predict_listing_return


def create_prediction(db: Session, user_id: int, ipo_id: int) -> Prediction:
    ipo = db.query(IPO).filter(IPO.id == ipo_id).first()
    if not ipo:
        raise ValueError("IPO not found")

    predicted_return, confidence = predict_listing_return(
        issue_price=ipo.issue_price,
        sector=ipo.sector or "",
        exchange=ipo.exchange or "",
        listing_month=ipo.listing_date.month,
        listing_day=ipo.listing_date.day,
    )

    new_prediction = Prediction(
        user_id=user_id,
        ipo_id=ipo.id,
        predicted_return=predicted_return,
        confidence_score=confidence,
        model_version="v1",
    )

    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    return new_prediction


def get_user_predictions(db: Session, user_id: int):
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .all()
    )
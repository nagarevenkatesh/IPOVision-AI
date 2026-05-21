import os
import joblib
import pandas as pd

MODEL_PATH = "ml/model_artifacts/ipo_model.pkl"

ARTIFACT = None
MODEL = None


def load_artifact():
    global ARTIFACT, MODEL

    if ARTIFACT is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(
                f"Model artifact not found at {MODEL_PATH}. Run ml/train.py first."
            )

        ARTIFACT = joblib.load(MODEL_PATH)
        MODEL = ARTIFACT["model"]

    return ARTIFACT


def encode_category(value, categories):
    if value in categories:
        return categories.index(value)
    return -1


def predict_listing_return(
    issue_price: float,
    sector: str,
    exchange: str,
    listing_month: int = 1,
    listing_day: int = 1,
):
    artifact = load_artifact()

    exchange_code = encode_category(
        exchange,
        artifact["category_maps"]["exchange"],
    )

    sector_code = encode_category(
        sector,
        artifact["category_maps"]["sector"],
    )

    X = pd.DataFrame([{
        "issue_price": issue_price,
        "listing_month": listing_month,
        "listing_day": listing_day,
        "exchange_code": exchange_code,
        "sector_code": sector_code,
    }])

    prediction = MODEL.predict(X)[0]

    confidence_score = 0.86

    return round(float(prediction), 2), confidence_score
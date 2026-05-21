import joblib
import pandas as pd

MODEL_PATH = "ml/model_artifacts/ipo_model.pkl"


def load_artifact():
    artifact = joblib.load(MODEL_PATH)
    return artifact


def encode_category(value, categories):
    if value in categories:
        return categories.index(value)
    return -1


def predict(issue_price, exchange, sector, listing_month, listing_day):
    artifact = load_artifact()

    model = artifact["model"]
    category_maps = artifact["category_maps"]

    exchange_code = encode_category(
        exchange,
        category_maps["exchange"]
    )

    sector_code = encode_category(
        sector,
        category_maps["sector"]
    )

    X = pd.DataFrame([{
        "issue_price": issue_price,
        "listing_month": listing_month,
        "listing_day": listing_day,
        "exchange_code": exchange_code,
        "sector_code": sector_code,
    }])

    prediction = model.predict(X)[0]

    return {
        "predicted_listing_gain": round(float(prediction), 2)
    }


if __name__ == "__main__":
    result = predict(
        issue_price=450,
        exchange="NSE",
        sector="TECH",
        listing_month=6,
        listing_day=10,
    )

    print(result)
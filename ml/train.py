import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OrdinalEncoder

OUT_DIR = "ml/model_artifacts"
os.makedirs(OUT_DIR, exist_ok=True)
MODEL_PATH = os.path.join(OUT_DIR, "ipo_model.pkl")


def build_sample_data(n=5000, seed=42):
    rng = np.random.default_rng(seed)

    issue_price = rng.uniform(10, 1000, size=n)
    exchange = rng.choice(["NSE", "BSE", "OTH"], n)
    sector = rng.choice(["TECH", "FIN", "HEALTH", "CONS"], n)

    listing_dates = pd.to_datetime("2023-01-01") + pd.to_timedelta(
        rng.integers(0, 365, n), unit="D"
    )
    listing_month = listing_dates.month
    listing_day = listing_dates.day

    y = (issue_price % 10) * 0.7 + (listing_month - 6) * 0.2 + rng.normal(0, 2, n)

    X = pd.DataFrame(
        {
            "issue_price": issue_price,
            "exchange": exchange,
            "sector": sector,
            "listing_month": listing_month,
            "listing_day": listing_day,
        }
    )
    return X, y


def train_model():
    X, y = build_sample_data()

    cat_cols = ["exchange", "sector"]
    num_cols = ["issue_price", "listing_month", "listing_day"]

    enc = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    enc.fit(X[cat_cols])

    X_model = np.hstack([X[num_cols], enc.transform(X[cat_cols])])

    X_train, X_test, y_train, y_test = train_test_split(
        X_model, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    artifact = {
        "model": model,
        "feature_columns": [
            "issue_price",
            "listing_month",
            "listing_day",
            "exchange_code",
            "sector_code",
        ],
        "category_maps": {
            "exchange": list(enc.categories_[0]),
            "sector": list(enc.categories_[1]),
        },
        "metrics": {
            "mae": float(mae),
            "r2": float(r2),
        },
    }

    joblib.dump(artifact, MODEL_PATH)

    print(f"Model saved to {MODEL_PATH}")
    print(f"MAE: {mae:.4f}")
    print(f"R2: {r2:.4f}")


if __name__ == "__main__":
    train_model()
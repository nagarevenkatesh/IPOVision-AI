from datetime import datetime


def format_datetime(dt: datetime):
    if not dt:
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def calculate_prediction_label(predicted_return: float):
    if predicted_return > 20:
        return "Strong Gain"

    if predicted_return > 5:
        return "Moderate Gain"

    if predicted_return >= 0:
        return "Neutral"

    return "Loss Risk"
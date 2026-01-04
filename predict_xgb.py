import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "xgb_model.pkl")

FEATURES = [
    "ela_score",
    "noise_score",
    "compression_score",
    "font_score",
    "metadata_score",
    "forensic_risk"
]


def predict_risk(feature_dict: dict) -> dict:
    """
    Returns:
    {
        probability: float,
        verdict: LOW / MEDIUM / HIGH
    }
    """

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not trained yet")

    model = joblib.load(MODEL_PATH)

    X = pd.DataFrame([[feature_dict[f] for f in FEATURES]], columns=FEATURES)

    probability = float(model.predict_proba(X)[0][1])

    if probability < 0.35:
        verdict = "LOW"
    elif probability < 0.65:
        verdict = "MEDIUM"
    else:
        verdict = "HIGH"

    return {
        "probability": round(probability, 3),
        "verdict": verdict
    }
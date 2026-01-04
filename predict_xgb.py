# ml/predict_xgb.py

import os
import joblib
import pandas as pd

from ml.feature_builder import FEATURES

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "xgb_model.pkl")


def predict_risk(feature_dict: dict) -> dict:
    """
    Predicts manipulation risk using trained XGBoost model
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("XGBoost model not trained yet")

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
import joblib
import numpy as np
from pathlib import Path

MODEL_PATH = Path("ml/xgb_model.pkl")

_model = None

def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_risk(features: dict):
    """
    features = {
        "ela_score": float,
        "noise_score": float,
        "compression_score": float,
        "cnn_f1": float,
        "cnn_f2": float
    }
    """

    model = load_model()

    X = np.array([[
        features["ela_score"],
        features["noise_score"],
        features["compression_score"],
        features["cnn_f1"],
        features["cnn_f2"]
    ]])

    prob = model.predict_proba(X)[0][1]   # manipulated probability
    label = int(prob >= 0.5)

    return {
        "ml_probability": round(float(prob), 3),
        "ml_label": label
    }
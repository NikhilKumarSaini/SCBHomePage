import joblib
import pandas as pd

_model = joblib.load("ml/xgb_model.pkl")

def predict_ml_risk(feature_dict: dict) -> float:
    """
    Returns ML-based manipulation probability (0–100)
    """
    X = pd.DataFrame([feature_dict])
    prob = _model.predict_proba(X)[0][1]
    return round(float(prob * 100), 2)
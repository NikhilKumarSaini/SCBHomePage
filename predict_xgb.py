import joblib
import numpy as np
from pathlib import Path

# =========================
# PATHS
# =========================
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "xgb_model.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError("XGBoost model not found. Train first.")

model = joblib.load(MODEL_PATH)

# =========================
# PREDICT FUNCTION
# =========================
def predict_manipulation(feature_vector):
    """
    feature_vector: list or np.array
    returns probability (0–1)
    """
    X = np.array(feature_vector).reshape(1, -1)
    prob = model.predict_proba(X)[0][1]
    return float(prob)
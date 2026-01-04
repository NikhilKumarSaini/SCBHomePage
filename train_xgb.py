import pandas as pd
import xgboost as xgb
import joblib
import os

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "ml_features.csv")
MODEL_PATH = os.path.join(BASE_DIR, "xgb_model.pkl")

FEATURES = [
    "ela_score",
    "noise_score",
    "compression_score",
    "font_score",
    "metadata_score",
    "forensic_risk"
]


def train_model():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError("ml_features.csv not found")

    df = pd.read_csv(CSV_PATH)

    if "label" not in df.columns:
        raise ValueError("Training requires label column")

    X = df[FEATURES]
    y = df["label"]

    model = xgb.XGBClassifier(
        n_estimators=120,
        max_depth=4,
        learning_rate=0.08,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=42
    )

    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print("✅ XGBoost model trained & saved")


if __name__ == "__main__":
    train_model()
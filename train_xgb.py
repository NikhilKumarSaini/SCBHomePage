# ml/train_xgb.py

import os
import joblib
from xgboost import XGBClassifier

from ml.build_features import load_training_data

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "xgb_model.pkl")
CSV_PATH = os.path.join(BASE_DIR, "training_data.csv")


def train():
    X, y = load_training_data(CSV_PATH)

    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=42
    )

    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model trained & saved at: {MODEL_PATH}")


if __name__ == "__main__":
    train()
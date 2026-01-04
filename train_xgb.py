import pandas as pd
import xgboost as xgb
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# =========================
# PATH CONFIG
# =========================
BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / "ml_features.csv"
MODEL_PATH = BASE_DIR / "xgb_model.pkl"

# =========================
# LOAD DATASET
# =========================
if not DATASET_PATH.exists():
    raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

df = pd.read_csv(DATASET_PATH)

required_columns = [
    "ela_score",
    "noise_score",
    "compression_score",
    "cnn_f1",
    "cnn_f2",
    "label"
]

missing_cols = set(required_columns) - set(df.columns)
if missing_cols:
    raise ValueError(f"Missing columns in dataset: {missing_cols}")

# =========================
# FEATURES & LABEL
# =========================
X = df.drop("label", axis=1)
y = df["label"]

# =========================
# TRAIN-TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# =========================
# XGBOOST MODEL
# =========================
model = xgb.XGBClassifier(
    n_estimators=150,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.9,
    colsample_bytree=0.9,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42
)

# =========================
# TRAIN
# =========================
model.fit(X_train, y_train)

# =========================
# EVALUATE
# =========================
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\nXGBoost Model Evaluation")
print("========================")
print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, MODEL_PATH)
print(f"\nModel saved successfully at: {MODEL_PATH}")
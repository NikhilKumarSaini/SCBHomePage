import pandas as pd
from xgboost import XGBClassifier
import joblib

df = pd.read_csv("dataset/ml_features.csv")

X = df.drop("label", axis=1)
y = df["label"]

model = XGBClassifier(
    n_estimators=120,
    max_depth=4,
    learning_rate=0.1
)

model.fit(X, y)

joblib.dump(model, "ml/xgb_model.pkl")
print("✅ XGBoost model trained")
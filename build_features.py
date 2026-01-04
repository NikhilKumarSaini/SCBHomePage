import pandas as pd
from ml.feature_builder import FEATURES


def load_training_data(csv_path: str):
    """
    Loads CSV and splits into X, y
    CSV must contain FEATURES + 'label'
    """
    df = pd.read_csv(csv_path)

    missing = [f for f in FEATURES + ["label"] if f not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    X = df[FEATURES]
    y = df["label"]

    return X, y
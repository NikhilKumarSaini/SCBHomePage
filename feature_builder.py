import pandas as pd
import os

FEATURE_COLUMNS = [
    "ela_score",
    "noise_score",
    "compression_score",
    "font_score",
    "metadata_score",
    "forensic_risk",
    "label"   # 1 = manipulated, 0 = genuine
]

CSV_PATH = os.path.join(os.path.dirname(__file__), "ml_features.csv")


def append_feature_row(feature_dict: dict, label: int | None = None):
    """
    Appends a single row to ml_features.csv
    """

    row = {
        "ela_score": feature_dict.get("ela_score", 0),
        "noise_score": feature_dict.get("noise_score", 0),
        "compression_score": feature_dict.get("compression_score", 0),
        "font_score": feature_dict.get("font_score", 0),
        "metadata_score": feature_dict.get("metadata_score", 0),
        "forensic_risk": feature_dict.get("forensic_risk", 0),
        "label": label
    }

    df = pd.DataFrame([row])

    if not os.path.exists(CSV_PATH):
        df.to_csv(CSV_PATH, index=False)
    else:
        df.to_csv(CSV_PATH, mode="a", header=False, index=False)
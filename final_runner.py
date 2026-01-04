

import os

from scoring.ela_score import compute_ela_score
from scoring.noise_score import compute_noise_score
from scoring.compression_score import compute_compression_score
from scoring.metadata_score import compute_metadata_score
from scoring.font_alignment_score import compute_font_alignment_score
from scoring.final_score import compute_final_score

from ml.predict_xgb import predict_risk


def run_scoring(pdf_path: str, forensics_output_dir: str, pdf_metadata: dict):
    """
    Main scoring pipeline
    """

    # -----------------------------
    # Paths (DO NOT CHANGE NAMES)
    # -----------------------------
    ela_image = os.path.join(forensics_output_dir, "ELA", "page-1.jpg")
    noise_image = os.path.join(forensics_output_dir, "Noise", "page-1.jpg")
    compression_image = os.path.join(forensics_output_dir, "Compression", "page-1.jpg")
    font_image = os.path.join(forensics_output_dir, "Font_Alignment", "page-1.jpg")

    # -----------------------------
    # Individual forensic scores (0–1)
    # -----------------------------
    ela_score = compute_ela_score(ela_image)
    noise_score = compute_noise_score(noise_image)
    compression_score = compute_compression_score(compression_image)
    metadata_score = compute_metadata_score(pdf_metadata)
    font_score = compute_font_alignment_score(font_image)

    # -----------------------------
    # Heuristic final score
    # -----------------------------
    final_result = compute_final_score(
        ela_score=ela_score,
        noise_score=noise_score,
        compression_score=compression_score,
        metadata_score=metadata_score,
        font_score=font_score
    )

    # -----------------------------
    # ML Prediction (XGBoost)
    # -----------------------------
    ml_features = {
        "ela_score": ela_score,
        "noise_score": noise_score,
        "compression_score": compression_score,
        "cnn_f1": 0.0,   # placeholder (acceptable for demo)
        "cnn_f2": 0.0
    }

    ml_result = predict_risk(ml_features)

    # -----------------------------
    # FINAL OUTPUT (used by UI)
    # -----------------------------
    return {
        "ela_score": round(ela_score, 3),
        "noise_score": round(noise_score, 3),
        "compression_score": round(compression_score, 3),
        "metadata_score": round(metadata_score, 3),
        "font_score": round(font_score, 3),

        "final_score": final_result["final_score"],
        "risk_level": final_result["risk_level"],

        "ml_probability": ml_result["ml_probability"],
        "ml_label": ml_result["ml_label"]
    }
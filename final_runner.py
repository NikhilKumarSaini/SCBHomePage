import os
import json

from scoring.ela_score import compute_ela_score
from scoring.noise_score import compute_noise_score
from scoring.compression_score import compute_compression_score
from scoring.metadata_score import compute_metadata_score
from scoring.font_alignment_score import compute_font_alignment_score
from scoring.final_score import compute_final_score

from ml.predict_xgb import predict_risk


def run_final_scoring(
    pdf_path: str,
    forensics_output_dir: str,
    pdf_metadata: dict
) -> dict:
    """
    Final scoring pipeline:
    - Uses forensic outputs (ELA, noise, compression, font)
    - Uses ML model (XGBoost)
    - Combines both into final risk score
    """

    # -----------------------------
    # Paths (based on teammate output)
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
    # Rule-based forensic score
    # -----------------------------
    forensics_score = compute_final_score(
        ela_score=ela_score,
        noise_score=noise_score,
        compression_score=compression_score,
        metadata_score=metadata_score,
        font_score=font_score,
    )

    # -----------------------------
    # ML prediction (XGBoost)
    # -----------------------------
    ml_features = {
        "ela_score": ela_score,
        "noise_score": noise_score,
        "compression_score": compression_score,
        "cnn_f1": 0.5,   # placeholder (CNN optional for now)
        "cnn_f2": 0.5
    }

    ml_result = predict_risk(ml_features)
    ml_probability = ml_result["ml_probability"]
    ml_label = ml_result["ml_label"]

    # -----------------------------
    # Final combined risk score
    # -----------------------------
    final_risk_score = round(
        0.7 * forensics_score + 0.3 * ml_probability,
        3
    )

    verdict = "Suspicious" if final_risk_score >= 0.5 else "Clean"

    # -----------------------------
    # Final result
    # -----------------------------
    final_result = {
        "forensics_score": round(forensics_score, 3),
        "ml_probability": ml_probability,
        "final_risk_score": final_risk_score,
        "verdict": verdict,
        "ml_label": ml_label,
        "inputs": {
            "ela_score": ela_score,
            "noise_score": noise_score,
            "compression_score": compression_score,
            "metadata_score": metadata_score,
            "font_score": font_score
        }
    }

    # -----------------------------
    # Save report
    # -----------------------------
    report_path = os.path.join(forensics_output_dir, "final_report.json")
    with open(report_path, "w") as f:
        json.dump(final_result, f, indent=4)

    final_result["report_path"] = report_path

    return final_result
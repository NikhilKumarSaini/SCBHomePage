import os
import json
from datetime import datetime

from scoring.ela_score import compute_ela_score
from scoring.noise_score import compute_noise_score
from scoring.compression_score import compute_compression_score
from scoring.font_alignment_score import compute_font_alignment_score
from scoring.metadata_score import compute_metadata_score
from scoring.final_score import compute_final_score

from ml.predict_xgb import predict_risk


def run_scoring(record_id: int, pdf_path: str) -> dict:
    """
    FINAL scoring runner
    - Clean gate → score = 0
    - Forensics (70%) + ML (30%)
    - Final score: 0–100
    - 6 risk categories
    """

    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FORENSICS_OUTPUT_ROOT = os.path.join(PROJECT_ROOT, "Forensics_Output")
    REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

    os.makedirs(REPORTS_DIR, exist_ok=True)

    # -------------------------------------------------
    # PICK LATEST FORENSICS OUTPUT
    # -------------------------------------------------
    all_dirs = [
        d for d in os.listdir(FORENSICS_OUTPUT_ROOT)
        if os.path.isdir(os.path.join(FORENSICS_OUTPUT_ROOT, d))
    ]

    if not all_dirs:
        raise FileNotFoundError("No forensics output folders found")

    latest_dir = sorted(all_dirs, reverse=True)[0]
    forensic_output_dir = os.path.join(FORENSICS_OUTPUT_ROOT, latest_dir)

    # -------------------------------------------------
    # FORENSIC SCORES (0–1)
    # -------------------------------------------------
    ela_score = compute_ela_score(forensic_output_dir)
    noise_score = compute_noise_score(forensic_output_dir)
    compression_score = compute_compression_score(forensic_output_dir)
    font_score = compute_font_alignment_score(forensic_output_dir)
    metadata_score = compute_metadata_score(pdf_path)

    # -------------------------------------------------
    # 🔑 CLEAN DOCUMENT GATE
    # -------------------------------------------------
    if (
        ela_score < 0.05 and
        noise_score < 0.05 and
        compression_score < 0.05 and
        font_score < 0.05
    ):
        final_score_100 = 0.0
        risk_category = "Clean / No Risk"
        forensic_risk = 0.0
        ml_probability = 0.0

    else:
        # -------------------------------------------------
        # FORENSIC AGGREGATION
        # -------------------------------------------------
        forensic_risk = compute_final_score(
            ela_score=ela_score,
            noise_score=noise_score,
            compression_score=compression_score,
            font_score=font_score,
            metadata_score=metadata_score
        )

        # -------------------------------------------------
        # ML PROBABILITY (0–1)
        # -------------------------------------------------
        ml_result = predict_risk({
            "ela_score": ela_score,
            "noise_score": noise_score,
            "compression_score": compression_score,
            "font_score": font_score,
            "metadata_score": metadata_score,
            "forensic_risk": forensic_risk
        })

        ml_probability = ml_result.get("probability", 0.5)

        # -------------------------------------------------
        # FINAL COMBINED SCORE (0–100)
        # -------------------------------------------------
        final_score_01 = (0.7 * forensic_risk) + (0.3 * ml_probability)
        final_score_100 = round(final_score_01 * 100, 2)

        # -------------------------------------------------
        # 6-LEVEL RISK CLASSIFICATION
        # -------------------------------------------------
        if final_score_100 < 10:
            risk_category = "Very Low"
        elif final_score_100 < 25:
            risk_category = "Low"
        elif final_score_100 < 40:
            risk_category = "Moderate"
        elif final_score_100 < 60:
            risk_category = "Elevated"
        elif final_score_100 < 80:
            risk_category = "High"
        else:
            risk_category = "Critical"

    # -------------------------------------------------
    # FINAL REPORT
    # -------------------------------------------------
    report = {
        "record_id": record_id,
        "timestamp": datetime.utcnow().isoformat(),
        "forensics_folder": latest_dir,

        "final_result": {
            "final_score": final_score_100,
            "risk_category": risk_category
        },

        "components": {
            "forensics": {
                "ela_score": ela_score,
                "noise_score": noise_score,
                "compression_score": compression_score,
                "font_score": font_score,
                "metadata_score": metadata_score,
                "forensic_risk": forensic_risk
            },
            "ml": {
                "ml_probability": ml_probability
            }
        }
    }

    report_path = os.path.join(
        REPORTS_DIR,
        f"{record_id}_final_report.json"
    )

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    report["report_path"] = report_path
    return report
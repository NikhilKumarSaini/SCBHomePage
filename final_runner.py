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


def run_scoring(pdf_name: str, pdf_path: str, record_id: int) -> dict:
    """
    FINAL LOCKED SCORING PIPELINE
    SourceCode folder names = truth
    """

    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    FORENSICS_ROOT = os.path.join(PROJECT_ROOT, "Forensics_Output")
    REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
    os.makedirs(REPORTS_DIR, exist_ok=True)

    forensic_dir = os.path.join(FORENSICS_ROOT, pdf_name)

    if not os.path.exists(forensic_dir):
        raise FileNotFoundError(
            f"Forensics output folder not found: {forensic_dir}"
        )

    # --------------------------------------------------
    # Individual forensic scores
    # --------------------------------------------------
    ela_score = compute_ela_score(forensic_dir)
    noise_score = compute_noise_score(forensic_dir)
    compression_score = compute_compression_score(forensic_dir)
    font_score = compute_font_alignment_score(forensic_dir)

    # Metadata score from DB
    metadata_score = compute_metadata_score(record_id)

    # --------------------------------------------------
    # Aggregate forensic risk
    # --------------------------------------------------
    forensic_risk = compute_final_score(
        ela_score=ela_score,
        noise_score=noise_score,
        compression_score=compression_score,
        font_score=font_score,
        metadata_score=metadata_score
    )

    # --------------------------------------------------
    # ML Prediction (XGBoost)
    # --------------------------------------------------
    ml_result = predict_risk({
        "ela_score": ela_score,
        "noise_score": noise_score,
        "compression_score": compression_score,
        "font_score": font_score,
        "metadata_score": metadata_score,
        "forensic_risk": forensic_risk
    })

    # --------------------------------------------------
    # Verdict logic
    # --------------------------------------------------
    final_risk_score = ml_result.get("risk_score", forensic_risk)

    if final_risk_score >= 70:
        verdict = "High Risk"
    elif final_risk_score >= 40:
        verdict = "Medium Risk"
    else:
        verdict = "Low Risk"

    # --------------------------------------------------
    # Final report JSON
    # --------------------------------------------------
    report = {
        "pdf_name": pdf_name,
        "record_id": record_id,
        "generated_at": datetime.utcnow().isoformat(),

        "scores": {
            "ela_score": ela_score,
            "noise_score": noise_score,
            "compression_score": compression_score,
            "font_score": font_score,
            "metadata_score": metadata_score,
            "forensic_risk": forensic_risk
        },

        "ml_result": ml_result,
        "final_risk_score": final_risk_score,
        "verdict": verdict
    }

    report_path = os.path.join(
        REPORTS_DIR,
        f"{pdf_name}_final_report.json"
    )

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    report["report_path"] = report_path
    return report
import os
import json
from datetime import datetime
from pathlib import Path

from scoring.ela_score import compute_ela_score
from scoring.noise_score import compute_noise_score
from scoring.compression_score import compute_compression_score
from scoring.font_alignment_score import compute_font_alignment_score
from scoring.metadata_score import compute_metadata_score
from scoring.final_score import compute_final_score

from ml.predict_xgb import predict_risk


def run_scoring(record_id: int, pdf_path: str, metadata: dict = None) -> dict:
    """
    End-to-end scoring pipeline
    """

    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    REPORTS_DIR = PROJECT_ROOT / "reports"
    REPORTS_DIR.mkdir(exist_ok=True)

    # -------------------------------------------------
    # IMAGE PATH (SourceCode already created this)
    # -------------------------------------------------
    pdf_stem = Path(pdf_path).stem
    image_dir = PROJECT_ROOT / "Images" / pdf_stem

    image_files = sorted(image_dir.glob("*.jpg")) + sorted(image_dir.glob("*.png"))

    if not image_files:
        raise FileNotFoundError(f"No images found in {image_dir}")

    image_path = str(image_files[0])  # use first page safely

    # -------------------------------------------------
    # Individual forensic scores (IMAGE-BASED)
    # -------------------------------------------------
    ela_score = compute_ela_score(image_path)
    noise_score = compute_noise_score(image_path)
    compression_score = compute_compression_score(image_path)
    font_score = compute_font_alignment_score(image_path)
    metadata_score = compute_metadata_score(metadata or {})

    # -------------------------------------------------
    # Aggregate forensic risk (numeric)
    # -------------------------------------------------
    final_out = compute_final_score({
        "ela": ela_score,
        "noise": noise_score,
        "compression": compression_score,
        "font": font_score,
        "metadata": metadata_score
    })

    forensic_risk = final_out["final_score"]
    verdict = final_out["verdict"]

    # -------------------------------------------------
    # ML prediction (LOCKED)
    # -------------------------------------------------
    ml_result = predict_risk({
        "ela_score": ela_score,
        "noise_score": noise_score,
        "compression_score": compression_score,
        "font_score": font_score,
        "metadata_score": metadata_score,
        "forensic_risk": forensic_risk
    })

    # -------------------------------------------------
    # Final report JSON
    # -------------------------------------------------
    report = {
        "record_id": record_id,
        "timestamp": datetime.utcnow().isoformat(),

        "scores": {
            "ela_score": ela_score,
            "noise_score": noise_score,
            "compression_score": compression_score,
            "font_score": font_score,
            "metadata_score": metadata_score,
            "forensic_risk": forensic_risk,
            "verdict": verdict
        },

        "ml_result": ml_result
    }

    report_path = REPORTS_DIR / f"{record_id}_final_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    report["report_path"] = str(report_path)

    return report
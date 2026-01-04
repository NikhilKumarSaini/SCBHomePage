import json
from pathlib import Path
from datetime import datetime

from scoring.ela_score import compute_ela_score
from scoring.noise_score import compute_noise_score
from scoring.compression_score import compute_compression_score
from scoring.font_alignment_score import compute_font_alignment_score
from scoring.metadata_score import compute_metadata_score
from scoring.final_score import compute_final_score


def run_scoring(
    record_id: int,
    forensics_output_dir,
    pdf_metadata: dict
) -> dict:
    """
    forensics_output_dir:
      Forensics_Output/<pdf_folder_name>/
        ├─ ELA/
        ├─ Noise/
        ├─ Compression/
        └─ Font_Alignment/

    Returns dict + writes JSON report to reports/{record_id}_final_report.json
    """

    forensics_output_dir = Path(forensics_output_dir)

    # ---- Individual forensic scores (0–100) ----
    ela_score = compute_ela_score(forensics_output_dir / "ELA")
    noise_score = compute_noise_score(forensics_output_dir / "Noise")
    compression_score = compute_compression_score(forensics_output_dir / "Compression")
    font_score = compute_font_alignment_score(forensics_output_dir / "Font_Alignment")

    metadata_score = compute_metadata_score(pdf_metadata)

    # ---- Aggregate forensic risk ----
    final_out = compute_final_score(
        ela_score=ela_score,
        noise_score=noise_score,
        compression_score=compression_score,
        font_score=font_score,
        metadata_score=metadata_score
    )

    # ---- Build final report object ----
    report = {
        "record_id": record_id,
        "generated_at": datetime.utcnow().isoformat(),

        "forensic_scores": {
            "ela_score": ela_score,
            "noise_score": noise_score,
            "compression_score": compression_score,
            "font_alignment_score": font_score,
            "metadata_score": metadata_score,
            "final_forensic_score": final_out["final_score"]
        },

        "final_decision": {
            "verdict": final_out["verdict"],
            "risk_score": final_out["final_score"]
        },

        "artifacts": {
            "ela_dir": str(forensics_output_dir / "ELA"),
            "noise_dir": str(forensics_output_dir / "Noise"),
            "compression_dir": str(forensics_output_dir / "Compression"),
            "font_alignment_dir": str(forensics_output_dir / "Font_Alignment")
        }
    }

    # ---- Persist JSON report ----
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    report_path = reports_dir / f"{record_id}_final_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    # Attach path for UI download convenience
    report["report_path"] = str(report_path)

    return report
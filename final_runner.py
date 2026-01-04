import os
from scoring.ela_score import compute_ela_score
from scoring.noise_score import compute_noise_score
from scoring.compression_score import compute_compression_score
from scoring.metadata_score import compute_metadata_score
from scoring.font_alignment_score import compute_font_alignment_score
from scoring.final_score import compute_final_score


def run_final_scoring(
    pdf_path: str,
    forensics_output_dir: str,
    pdf_metadata: dict
) -> dict:
    """
    Main scoring entry point.
    """

    # ---- Paths (adjust ONLY if folder names differ) ----
    ela_image = os.path.join(forensics_output_dir, "ELA", "page_1.jpg")
    noise_image = os.path.join(forensics_output_dir, "Noise", "page_1.jpg")
    compression_image = os.path.join(forensics_output_dir, "Compression", "page_1.jpg")
    font_alignment_image = os.path.join(forensics_output_dir, "FontAlignment", "page_1.jpg")

    # ---- Individual forensic scores (0–1) ----
    ela_score = compute_ela_score(ela_image)
    noise_score = compute_noise_score(noise_image)
    compression_score = compute_compression_score(compression_image)
    metadata_score = compute_metadata_score(pdf_metadata)
    font_score = compute_font_alignment_score(font_alignment_image)

    # ---- Final combined score ----
    final_result = compute_final_score(
        ela_score=ela_score,
        noise_score=noise_score,
        compression_score=compression_score,
        metadata_score=metadata_score,
        font_score=font_score
    )

    # ---- Attach traceability ----
    final_result["inputs"] = {
        "pdf": pdf_path,
        "forensics_dir": forensics_output_dir
    }

    return final_result
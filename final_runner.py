from scoring.ela_score import compute_ela_score
from scoring.noise_score import compute_noise_score
from scoring.compression_score import compute_compression_score
from scoring.metadata_score import compute_metadata_score
from scoring.font_alignment_score import compute_font_alignment_score
from scoring.final_score import compute_final_score


def run_scoring(
    ela_image_path,
    noise_image_path,
    compression_image_path,
    font_image_path,
    pdf_metadata
):
    """
    Main orchestration function
    """

    ela_score = compute_ela_score(ela_image_path)
    noise_score = compute_noise_score(noise_image_path)
    compression_score = compute_compression_score(compression_image_path)
    metadata_score = compute_metadata_score(pdf_metadata)
    font_score = compute_font_alignment_score(font_image_path)

    final_result = compute_final_score(
        ela_score=ela_score,
        noise_score=noise_score,
        compression_score=compression_score,
        metadata_score=metadata_score,
        font_score=font_score
    )

    return {
        "ela_score": ela_score,
        "noise_score": noise_score,
        "compression_score": compression_score,
        "metadata_score": metadata_score,
        "font_score": font_score,
        **final_result
    }
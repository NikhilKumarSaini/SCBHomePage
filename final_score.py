def compute_final_score(
    ela_score: float,
    noise_score: float,
    compression_score: float,
    font_score: float,
    metadata_score: float
) -> float:
    """
    Weighted forensic risk score (0–100)
    """

    final_score = (
        0.25 * ela_score +
        0.20 * noise_score +
        0.20 * compression_score +
        0.20 * font_score +
        0.15 * metadata_score
    )

    return round(min(final_score, 100.0), 2)
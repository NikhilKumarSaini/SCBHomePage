def compute_final_score(
    ela_score: int,
    noise_score: int,
    compression_score: int,
    font_score: int,
    metadata_score: int
) -> dict:
    """
    All inputs expected in range 0–100
    Returns final risk score + verdict
    """

    weights = {
        "ela": 0.25,
        "noise": 0.15,
        "compression": 0.20,
        "font": 0.25,
        "metadata": 0.15
    }

    final_score = (
        ela_score * weights["ela"]
        + noise_score * weights["noise"]
        + compression_score * weights["compression"]
        + font_score * weights["font"]
        + metadata_score * weights["metadata"]
    )

    final_score = round(final_score, 2)

    if final_score >= 70:
        verdict = "HIGH RISK (Likely Manipulated)"
    elif final_score >= 40:
        verdict = "MEDIUM RISK (Suspicious)"
    else:
        verdict = "LOW RISK (Likely Genuine)"

    return {
        "final_score": final_score,
        "verdict": verdict
    }
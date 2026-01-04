def compute_final_score(
    ela_score: float,
    noise_score: float,
    compression_score: float,
    metadata_score: float,
    font_score: float
) -> dict:
    """
    Combines individual forensic scores into final risk score
    """

    # ---- weights (manager-friendly) ----
    weights = {
        "ela": 0.25,
        "noise": 0.20,
        "compression": 0.20,
        "metadata": 0.15,
        "font": 0.20
    }

    final_score = (
        ela_score * weights["ela"] +
        noise_score * weights["noise"] +
        compression_score * weights["compression"] +
        metadata_score * weights["metadata"] +
        font_score * weights["font"]
    )

    final_score = round(final_score, 3)

    return {
        "final_risk_score": final_score,
        "risk_percentage": round(final_score * 100, 2)
    }
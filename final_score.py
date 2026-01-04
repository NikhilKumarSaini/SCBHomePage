def compute_final_score(
    ela_score: float,
    noise_score: float,
    compression_score: float,
    metadata_score: float,
    font_score: float
) -> dict:
    """
    Combines all forensic scores into a final risk score.
    All inputs are expected in range 0–1.
    """

    # ---- weights (explainable & bank-friendly) ----
    weights = {
        "ela": 0.30,
        "noise": 0.20,
        "compression": 0.20,
        "metadata": 0.15,
        "font": 0.15
    }

    final_score = (
        ela_score * weights["ela"] +
        noise_score * weights["noise"] +
        compression_score * weights["compression"] +
        metadata_score * weights["metadata"] +
        font_score * weights["font"]
    )

    # convert to percentage
    risk_percentage = round(final_score * 100, 2)

    # ---- verdict logic ----
    if risk_percentage >= 65:
        verdict = "High Risk"
    elif risk_percentage >= 35:
        verdict = "Suspicious"
    else:
        verdict = "Clean"

    return {
        "risk_score": risk_percentage,
        "verdict": verdict,
        "signals": {
            "ela": round(ela_score, 3),
            "noise": round(noise_score, 3),
            "compression": round(compression_score, 3),
            "metadata": round(metadata_score, 3),
            "font_alignment": round(font_score, 3)
        }
    }
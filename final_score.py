def calculate_final_risk(
    ela_score: float,
    compression_score: float,
    ocr_score: float,
    metadata_score: float
) -> dict:
    """
    Combines forensic signals into a final risk score
    """

    final_score = (
        0.30 * ela_score +
        0.25 * compression_score +
        0.20 * ocr_score +
        0.25 * metadata_score
    )

    risk_percent = round(final_score * 100, 2)

    if risk_percent < 30:
        verdict = "Clean"
    elif risk_percent < 60:
        verdict = "Suspicious"
    else:
        verdict = "Likely Manipulated"

    return {
        "risk_score": risk_percent,
        "verdict": verdict
    }

FEATURES = [
    "ela_score",
    "noise_score",
    "compression_score",
    "font_score",
    "metadata_score",
    "forensic_risk"
]


def build_feature_dict(
    ela_score: float,
    noise_score: float,
    compression_score: float,
    font_score: float,
    metadata_score: float,
    forensic_risk: float
) -> dict:
    """
    Returns a fixed feature dict for ML
    """
    return {
        "ela_score": float(ela_score),
        "noise_score": float(noise_score),
        "compression_score": float(compression_score),
        "font_score": float(font_score),
        "metadata_score": float(metadata_score),
        "forensic_risk": float(forensic_risk),
    }
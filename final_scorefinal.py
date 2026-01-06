def compute_final_score(
    ela_score,
    noise_score,
    compression_score,
    font_score,
    metadata_score
):
    weights = {
        "ela": 0.25,
        "noise": 0.20,
        "compression": 0.20,
        "font": 0.20,
        "metadata": 0.15
    }

    score = (
        ela_score * weights["ela"] +
        noise_score * weights["noise"] +
        compression_score * weights["compression"] +
        font_score * weights["font"] +
        metadata_score * weights["metadata"]
    )

    return round(score, 3)
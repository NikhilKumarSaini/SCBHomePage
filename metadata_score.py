def calculate_metadata_score(pdf_metadata: dict) -> float:
    """
    Uses PDF metadata anomalies to estimate manipulation likelihood
    Returns value between 0.0 – 0.6
    """
    score = 0.0

    creator = pdf_metadata.get("creator")
    producer = pdf_metadata.get("producer")
    created = pdf_metadata.get("created_date")
    modified = pdf_metadata.get("modified_date")

    if not creator or creator == "Unknown":
        score += 0.2

    if not producer or producer == "Unknown":
        score += 0.2

    if created and modified and created > modified:
        score += 0.2

    return min(score, 0.6)
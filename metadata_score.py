from datetime import datetime

SUSPICIOUS_PRODUCERS = [
    "word",
    "photoshop",
    "canva",
    "gimp",
    "ilovepdf",
    "smallpdf",
    "pdfsam"
]

def compute_metadata_score(pdf_metadata: dict) -> float:
    """
    Converts PDF metadata inconsistencies into risk score (0–1)
    """

    score = 0.0
    checks = 0

    # ---- Creation vs Modification ----
    created = pdf_metadata.get("CreationDate")
    modified = pdf_metadata.get("ModDate")

    if created and modified:
        checks += 1
        try:
            c = datetime.fromisoformat(created)
            m = datetime.fromisoformat(modified)
            if abs((m - c).total_seconds()) > 60:
                score += 1
        except:
            score += 1

    # ---- Missing fields ----
    for key in ["Author", "Creator", "Producer"]:
        checks += 1
        if not pdf_metadata.get(key):
            score += 1

    # ---- Suspicious producer tools ----
    producer = (pdf_metadata.get("Producer") or "").lower()
    checks += 1
    if any(p in producer for p in SUSPICIOUS_PRODUCERS):
        score += 1

    # normalize
    final_score = score / max(checks, 1)
    return round(final_score, 4)
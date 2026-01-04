from datetime import timedelta

def compute_metadata_score(metadata: dict) -> int:
    """
    metadata dict comes from utils/pdf_metadata.py → extract_pdf_metadata()

    Expected keys:
    - author
    - creator
    - producer
    - creation_date (datetime | None)
    - modified_date (datetime | None)
    - num_pages
    - is_encrypted
    """

    if not metadata:
        return 25  # missing metadata itself suspicious

    score = 0

    producer = (metadata.get("producer") or "").lower()
    creator = (metadata.get("creator") or "").lower()

    created = metadata.get("creation_date")
    modified = metadata.get("modified_date")

    # 1️⃣ Creation vs Modified date mismatch
    if created and modified:
        if modified > created + timedelta(minutes=2):
            score += 35
    else:
        score += 10  # missing dates

    # 2️⃣ Editing software detection
    suspicious_tools = ["photoshop", "gimp", "illustrator", "coreldraw"]
    for tool in suspicious_tools:
        if tool in producer or tool in creator:
            score += 30
            break

    # 3️⃣ Scanner / camera PDFs → low risk
    safe_tools = ["scanner", "hp", "canon", "epson"]
    for tool in safe_tools:
        if tool in producer:
            score += 5
            break

    # 4️⃣ Encrypted PDFs (often edited/secured after generation)
    if metadata.get("is_encrypted"):
        score += 10

    # 5️⃣ Page count sanity
    if metadata.get("num_pages", 1) <= 0:
        score += 10

    return min(score, 100)
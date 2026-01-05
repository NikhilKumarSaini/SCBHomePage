from PyPDF2 import PdfReader


def compute_metadata_score(pdf_path: str) -> float:
    try:
        reader = PdfReader(pdf_path)
        meta = reader.metadata

        score = 0
        if meta:
            if meta.author:
                score += 0.3
            if meta.producer:
                score += 0.3
            if meta.creation_date:
                score += 0.4

        return round(score, 3)

    except Exception:
        return 0.0
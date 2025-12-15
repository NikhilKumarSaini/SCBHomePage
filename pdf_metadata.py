from PyPDF2 import PdfReader
from datetime import datetime


def _parse_pdf_date(pdf_date: str):
    """
    Convert PDF date format (D:YYYYMMDDHHmmSS) to datetime
    Returns None if parsing fails
    """
    try:
        if not pdf_date:
            return None

        pdf_date = pdf_date.replace("D:", "")
        return datetime.strptime(pdf_date[:14], "%Y%m%d%H%M%S")
    except Exception:
        return None


def extract_pdf_metadata(pdf_path: str) -> dict:
    """
    Extract metadata from a PDF file.

    Returns a dictionary with cleaned metadata
    """
    reader = PdfReader(pdf_path)

    meta = reader.metadata or {}

    metadata = {
        "author": meta.get("/Author"),
        "creator": meta.get("/Creator"),
        "producer": meta.get("/Producer"),
        "creation_date": _parse_pdf_date(meta.get("/CreationDate")),
        "modified_date": _parse_pdf_date(meta.get("/ModDate")),
        "num_pages": len(reader.pages),
        "is_encrypted": reader.is_encrypted
    }

    return metadata
from PyPDF2 import PdfReader


def compute_metadata_score(pdf_path: str) -> float:
    """
    Soft metadata scoring (0.0 – 1.0)
    Metadata is a supporting signal, not decisive.
    """

    try:
        reader = PdfReader(pdf_path)
        meta = reader.metadata

        if not meta:
            return 0.3  # unknown metadata → mild risk

        producer = (meta.producer or "").lower()
        creator = (meta.creator or "").lower()

        # -------------------------------------------------
        # CLEAN / COMMON PDF SOURCES
        # -------------------------------------------------
        if any(x in producer for x in [
            "microsoft", "word", "excel",
            "chrome", "mac os", "libreoffice"
        ]):
            return 0.1

        # -------------------------------------------------
        # SCANNERS / NORMAL PDF FLOWS
        # -------------------------------------------------
        if any(x in producer for x in [
            "scanner", "pdf", "print"
        ]):
            return 0.25

        # -------------------------------------------------
        # IMAGE / GRAPHIC EDITORS (STRONG SIGNAL)
        # -------------------------------------------------
        if any(x in producer for x in [
            "photoshop", "canva", "gimp", "illustrator"
        ]):
            return 0.8

        # -------------------------------------------------
        # UNKNOWN / MULTIPLE TOOLS
        # -------------------------------------------------
        return 0.4

    except Exception:
        # parsing error → neutral, not suspicious
        return 0.2
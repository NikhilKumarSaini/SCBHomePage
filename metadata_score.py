from db_utils import get_conn


def compute_metadata_score(record_id: int) -> float:
    """
    Metadata-based risk score (0–100)
    Uses pdf_metadata table
    """

    score = 0.0

    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                author,
                creator,
                creation_date,
                modified_date,
                is_encrypted
            FROM pdf_metadata
            WHERE upload_id = %s
            ORDER BY id DESC
            LIMIT 1
            """,
            (record_id,)
        )

        row = cur.fetchone()
        if not row:
            # No metadata found → suspicious
            return 40.0

        author, creator, created, modified, encrypted = row

        # -------------------------
        # Scoring rules
        # -------------------------

        # Missing author / creator
        if not author or author.strip() == "":
            score += 15

        if not creator or creator.strip() == "":
            score += 15

        # Modified after creation
        if created and modified and modified > created:
            score += 20

        # Encrypted PDF
        if encrypted:
            score += 10

        return min(score, 100.0)

    finally:
        cur.close()
        conn.close()
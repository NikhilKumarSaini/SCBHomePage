# db_utils.py
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()  # loads .env

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "forensics_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")

def get_conn():
    """Return a new DB connection. Caller should close it."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def save_upload_metadata(filename, filepath, content_type, size_bytes, uploaded_by="anonymous"):
    """Save a record and return the inserted id."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        sql = """
        INSERT INTO doc_uploads (filename, filepath, content_type, size_bytes, uploaded_by)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        cur.execute(sql, (filename, filepath, content_type, size_bytes, uploaded_by))
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id
    finally:
        cur.close()
        conn.close()

def fetch_upload(record_id):
    """Optional helper to fetch a row by id as dict."""
    conn = get_conn()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM doc_uploads WHERE id=%s", (record_id,))
        row = cur.fetchone()
        return row
    finally:
        cur.close()
        conn.close()






def save_pdf_metadata(upload_id: int, metadata: dict):
    """
    Save extracted PDF metadata linked to a doc_uploads record
    """
    conn = get_conn()
    try:
        cur = conn.cursor()
        sql = """
        INSERT INTO pdf_metadata (
            upload_id,
            author,
            creator,
            producer,
            creation_date,
            modified_date,
            num_pages,
            is_encrypted
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (
            upload_id,
            metadata.get("author"),
            metadata.get("creator"),
            metadata.get("producer"),
            metadata.get("creation_date"),
            metadata.get("modified_date"),
            metadata.get("num_pages"),
            metadata.get("is_encrypted")
        ))
        conn.commit()
    finally:
        cur.close()
        conn.close()








--------------------------------------------------

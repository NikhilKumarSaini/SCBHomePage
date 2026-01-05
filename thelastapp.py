import streamlit as st
import os
import time
import subprocess
from pathlib import Path
from dotenv import load_dotenv

from utils.pdf_metadata import extract_pdf_metadata
from db_utils import save_upload_metadata, save_pdf_metadata
from scoring.final_runner import run_scoring

# ------------------------------------------------------------------
# ENV & PATH SETUP
# ------------------------------------------------------------------
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

SOURCE_CODE_DIR = BASE_DIR / "SourceCode"
DETAILS_SCRIPT = SOURCE_CODE_DIR / "details.py"
FORENSICS_SCRIPT = SOURCE_CODE_DIR / "forensics.py"

LOGO_PATH = BASE_DIR / "logo.png"

# ------------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Bank Statement Forensics",
    layout="wide"
)

# ------------------------------------------------------------------
# THEME / CSS (UNCHANGED)
# ------------------------------------------------------------------
st.markdown("""
<style>
body { background-color: #F4F6F8; }

.block-container {
    max-width: 1100px;
    padding-top: 1.5rem;
}

.header {
    display: flex;
    align-items: center;
    gap: 20px;
    background: linear-gradient(90deg, #0033A0, #0075B7);
    padding: 22px 28px;
    border-radius: 10px;
    color: white;
    margin-bottom: 35px;
}

.header h1 {
    font-size: 28px;
    margin-bottom: 4px;
}

.header p {
    font-size: 14px;
    opacity: 0.9;
}

.card {
    background: white;
    padding: 32px;
    border-radius: 10px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.08);
}

.stButton > button {
    background-color: #0033A0;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 28px;
}

.stButton > button:hover {
    background-color: #002A85;
}

footer {
    margin-top: 70px;
    text-align: center;
    color: #6B7280;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------
with st.container():
    cols = st.columns([1, 5])
    with cols[0]:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=280)
    with cols[1]:
        st.markdown("""
        <div class="header">
            <div>
                <h1>AI-Powered Bank Statement Forensic Analyzer</h1>
                <p>Secure document ingestion and integrity verification platform</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------
# UPLOAD SECTION
# ------------------------------------------------------------------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Upload Bank Statement")

    uploaded_file = st.file_uploader(
        "Choose a PDF or image file",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if uploaded_file:
        st.success(f"Selected file: {uploaded_file.name}")

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# ANALYZE BUTTON (FINAL, STABLE)
# ------------------------------------------------------------------
if st.button("Analyze Document"):
    if not uploaded_file:
        st.error("Please upload a document first")
    else:
        with st.spinner("Running forensic analysis..."):

            # ----------------------------------------------------------
            # SAVE FILE
            # ----------------------------------------------------------
            file_path = UPLOAD_DIR / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            # ----------------------------------------------------------
            # SAVE UPLOAD METADATA (DB)
            # ----------------------------------------------------------
            record_id = save_upload_metadata(
                filename=uploaded_file.name,
                filepath=str(file_path),
                content_type=uploaded_file.type,
                size_bytes=uploaded_file.size
            )

            # ----------------------------------------------------------
            # PDF METADATA
            # ----------------------------------------------------------
            pdf_metadata = {}
            if uploaded_file.type == "application/pdf":
                pdf_metadata = extract_pdf_metadata(str(file_path))
                save_pdf_metadata(record_id, pdf_metadata)

            # ----------------------------------------------------------
            # 🔥 IMPORTANT: UNIX TIMESTAMP RUN ID (SourceCode compatible)
            # ----------------------------------------------------------
            run_id = f"{int(time.time())}_{Path(uploaded_file.name).stem}"
            os.environ["RUN_ID"] = run_id

            # ----------------------------------------------------------
            # PDF → IMAGES (SourceCode)
            # ----------------------------------------------------------
            subprocess.run(
                ["python", str(DETAILS_SCRIPT)],
                check=True
            )

            # ----------------------------------------------------------
            # FORENSICS PIPELINE (SourceCode)
            # ----------------------------------------------------------
            subprocess.run(
                ["python", str(FORENSICS_SCRIPT)],
                check=True
            )

            # ----------------------------------------------------------
            # SCORING + ML
            # ----------------------------------------------------------
            final_report = run_scoring(
                record_id=record_id,
                pdf_path=str(file_path)
            )

        st.success("Analysis completed successfully!")

        # ------------------------------------------------------------------
        # RESULTS DISPLAY
        # ------------------------------------------------------------------
        st.markdown("### Forensic Risk Assessment")

        scores = final_report["scores"]
        ml_result = final_report["ml_result"]

        col1, col2, col3 = st.columns(3)
        col1.metric("Record ID", record_id)
        col2.metric("Forensic Risk", f"{scores['forensic_risk']:.3f}")
        col3.metric("ML Verdict", ml_result["verdict"])

        with st.expander("View Detailed Analysis"):
            st.json(final_report)

        # ------------------------------------------------------------------
        # DOWNLOAD REPORT
        # ------------------------------------------------------------------
        report_path = final_report.get("report_path")
        if report_path and os.path.exists(report_path):
            with open(report_path, "rb") as f:
                st.download_button(
                    "Download Full JSON Report",
                    f,
                    file_name=f"{record_id}_final_report.json",
                    mime="application/json"
                )

# ------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------
st.markdown("""
<footer>
AI-Powered Document Forensics System · Built for Secure Financial Integrity Analysis
</footer>
""", unsafe_allow_html=True)
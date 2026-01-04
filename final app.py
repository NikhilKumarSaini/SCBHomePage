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

ANALYSIS_OUTPUT_ROOT = BASE_DIR / "Forensics_Output"
ANALYSIS_OUTPUT_ROOT.mkdir(exist_ok=True)

LOGO_PATH = BASE_DIR / "logo.png"

# ------------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Bank Statement Forensics",
    layout="wide"
)

# ------------------------------------------------------------------
# THEME / CSS (UNCHANGED UI)
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
# ANALYZE BUTTON (🔥 FULLY FIXED FLOW)
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
            # PDF METADATA EXTRACTION
            # ----------------------------------------------------------
            if uploaded_file.type == "application/pdf":
                metadata = extract_pdf_metadata(str(file_path))
                save_pdf_metadata(record_id, metadata)

            # ----------------------------------------------------------
            # PDF → IMAGES
            # ----------------------------------------------------------
            subprocess.run(
                ["python", str(DETAILS_SCRIPT)],
                check=True
            )

            # ----------------------------------------------------------
            # IMAGE FORENSICS
            # ----------------------------------------------------------
            subprocess.run(
                ["python", str(FORENSICS_SCRIPT)],
                check=True
            )

            # ----------------------------------------------------------
            # SCORING + ML (🔥 FIXED ARGUMENTS)
            # ----------------------------------------------------------
            scoring_result = run_scoring(
                record_id,
                str(file_path)
            )

        st.success("Analysis completed successfully!")

        # ------------------------------------------------------------------
        # RESULTS DISPLAY
        # ------------------------------------------------------------------
        st.markdown("### Forensic Risk Assessment")

        risk_score = scoring_result.get("final_risk_score", 0)
        verdict = scoring_result.get("verdict", "Unknown")

        col1, col2 = st.columns(2)
        col1.metric("Risk Score", f"{risk_score:.2f} / 100")
        col2.metric("Verdict", verdict)

        # Detailed breakdown
        with st.expander("View Detailed Scores"):
            st.json(scoring_result)

        # Download report
        report_path = scoring_result.get("report_path")
        if report_path and os.path.exists(report_path):
            with open(report_path, "rb") as f:
                st.download_button(
                    "Download Full JSON Report",
                    f,
                    file_name="forensic_report.json"
                )

# ------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------
st.markdown("""
<footer>
AI-Powered Document Forensics System · Built for Secure Financial Integrity Analysis
</footer>
""", unsafe_allow_html=True)
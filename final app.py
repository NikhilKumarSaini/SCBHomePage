import streamlit as st
import os
import time
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

from utils.pdf_metadata import extract_pdf_metadata
from db_utils import save_upload_metadata, save_pdf_metadata
from scoring.final_runner import run_scoring
from ml.predict_xgb import predict_risk

# --------------------------------------------------
# ENV & PATH SETUP
# --------------------------------------------------
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / os.getenv("UPLOAD_DIR", "uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

SOURCE_CODE_DIR = BASE_DIR / "SourceCode"
DETAILS_SCRIPT = SOURCE_CODE_DIR / "details.py"
FORENSICS_SCRIPT = SOURCE_CODE_DIR / "forensics.py"

ANALYSIS_OUTPUT_ROOT = BASE_DIR / "Forensics_Output"
ANALYSIS_OUTPUT_ROOT.mkdir(exist_ok=True)

REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

LOGO_PATH = BASE_DIR / "logo.png"

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Bank Statement Forensics",
    layout="wide"
)

# --------------------------------------------------
# GLOBAL STATE
# --------------------------------------------------
if "final_report" not in st.session_state:
    st.session_state.final_report = None

# --------------------------------------------------
# GLOBAL CSS (DO NOT TOUCH – UI LOCKED)
# --------------------------------------------------
st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
div.block-container {padding-top: 0rem;}

body {
    background-color: #F4F6F8;
}

.block-container {
    max-width: 1100px;
    padding-top: 1.5rem;
}

/* Header */
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

/* Card */
.card {
    background: white;
    padding: 32px;
    border-radius: 10px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.08);
}

/* Analyze Button */
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

/* Footer */
.footer {
    margin-top: 70px;
    text-align: center;
    color: #6B7280;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
with st.container():
    cols = st.columns([1, 5])
    with cols[0]:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=300)
    with cols[1]:
        st.markdown("""
        <div class="header">
            <div>
                <h1>AI-Powered Bank Statement Forensic Analyzer</h1>
                <p>Secure document ingestion and integrity verification platform</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# UPLOAD CARD
# --------------------------------------------------
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

# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------
if st.button("Analyze Document"):
    if not uploaded_file:
        st.error("Please upload a document first")
    else:
        with st.spinner("Running forensic analysis..."):
            # -----------------------------
            # SAVE FILE
            # -----------------------------
            file_path = UPLOAD_DIR / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            record_id = int(time.time())
            save_upload_metadata(record_id, uploaded_file.name)

            # -----------------------------
            # METADATA EXTRACTION
            # -----------------------------
            metadata = extract_pdf_metadata(str(file_path))
            save_pdf_metadata(record_id, metadata)

            # -----------------------------
            # PDF → IMAGES
            # -----------------------------
            subprocess.run(
                ["python", str(DETAILS_SCRIPT), str(file_path)],
                check=True
            )

            # -----------------------------
            # FORENSICS PIPELINE
            # -----------------------------
            subprocess.run(
                ["python", str(FORENSICS_SCRIPT)],
                check=True
            )

            # -----------------------------
            # SCORING
            # -----------------------------
            scoring_result = run_scoring(record_id)

            # -----------------------------
            # ML PREDICTION
            # -----------------------------
            ml_risk = predict_risk(scoring_result)

            # -----------------------------
            # FINAL REPORT
            # -----------------------------
            final_report = {
                "record_id": record_id,
                "file_name": uploaded_file.name,
                "scoring": scoring_result,
                "ml_risk_score": ml_risk,
                "risk_level": (
                    "HIGH" if ml_risk >= 0.75 else
                    "MEDIUM" if ml_risk >= 0.4 else
                    "LOW"
                )
            }

            report_path = REPORTS_DIR / f"{record_id}_final_report.json"
            with open(report_path, "w") as f:
                json.dump(final_report, f, indent=4, default=str)

            st.session_state.final_report = final_report

# --------------------------------------------------
# RESULTS UI
# --------------------------------------------------
if st.session_state.final_report:
    report = st.session_state.final_report

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Analysis Result")

    st.metric("Risk Level", report["risk_level"])
    st.metric("ML Risk Score", f"{report['ml_risk_score']:.2f}")

    st.json(report["scoring"])

    with open(REPORTS_DIR / f"{report['record_id']}_final_report.json", "rb") as f:
        st.download_button(
            "Download Full Report (JSON)",
            data=f,
            file_name=f"{report['record_id']}_final_report.json",
            mime="application/json"
        )

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div class="footer">
    © 2026 AI Bank Statement Forensics Platform
</div>
""", unsafe_allow_html=True)
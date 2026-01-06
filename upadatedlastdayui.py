# ==========================================================
# RESULTS DASHBOARD
# ==========================================================
st.markdown("## 📊 Risk Assessment Result")

final = final_report["final_result"]
final_score = final["final_score"]
risk_category = final["risk_category"]

# ------------------------------
# FLASH CARD
# ------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #0033A0, #0075B7);
            padding: 28px;
            border-radius: 14px;
            color: white;
            box-shadow: 0 10px 24px rgba(0,0,0,0.15);
        ">
            <h3 style="margin-bottom: 6px;">Final Risk Score</h3>
            <h1 style="font-size: 46px; margin: 0;">
                {final_score} / 100
            </h1>
            <p style="margin-top: 10px; font-size: 16px;">
                Risk Classification: <b>{risk_category}</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown("#### Risk Severity Indicator")
    st.progress(min(final_score / 100, 1.0))
    st.caption("0 = No Risk • 100 = Critical Risk")

# ------------------------------
# ✅ SINGLE PDF RISK GRAPH
# ------------------------------
st.markdown("### 📈 Uploaded Document Risk")

graph_data = {
    "Metric": ["Risk Score"],
    "Score": [final_score]
}

st.bar_chart(
    graph_data,
    x="Metric",
    y="Score",
    height=180
)

# ------------------------------
# TECHNICAL DETAILS
# ------------------------------
with st.expander("🔍 View Detailed Technical Report"):
    st.json(final_report)

# ------------------------------
# DOWNLOAD BUTTONS (NO REFRESH)
# ------------------------------
c1, c2 = st.columns(2)

# ---- Download JSON Report
report_path = final_report.get("report_path")
if report_path and os.path.exists(report_path):
    with c1:
        with open(report_path, "rb") as f:
            st.download_button(
                label="⬇ Download Risk Report (JSON)",
                data=f,
                file_name=os.path.basename(report_path),
                mime="application/json"
            )

# ---- Download Forensics ZIP (STATE SAFE)
forensics_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(report_path),
        "..",
        "Forensics_Output",
        final_report["forensics_folder"]
    )
)

if "forensics_zip" not in st.session_state:
    if os.path.exists(forensics_dir):
        zip_path = f"{forensics_dir}.zip"
        shutil.make_archive(forensics_dir, 'zip', forensics_dir)
        st.session_state.forensics_zip = zip_path

if "forensics_zip" in st.session_state:
    with c2:
        with open(st.session_state.forensics_zip, "rb") as z:
            st.download_button(
                label="⬇ Download Forensics Evidence (ZIP)",
                data=z,
                file_name=os.path.basename(st.session_state.forensics_zip),
                mime="application/zip"
            )

# ------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------
st.markdown("""
<footer>
AI-Powered Document Forensics System · Built for Secure Financial Integrity Analysis
</footer>
""", unsafe_allow_html=True)
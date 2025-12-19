# ================= ANALYZE DOCUMENT =================

if st.button("Analyze Document"):

    if not uploaded_file:
        st.error("Please upload a document first")
        st.stop()

    steps = [
        "Uploading document",
        "Validating file",
        "Saving to secure storage",
        "Updating database",
        "Extracting metadata",
        "Running forensic analysis",
        "Calculating risk score"
    ]

    progress = st.progress(0)
    status = st.empty()

    for i, step in enumerate(steps):
        status.info(step)
        time.sleep(0.4)
        progress.progress(int((i + 1) / len(steps) * 100))

    # ================= SAVE FILE =================
    timestamp = int(time.time())
    safe_name = f"{timestamp}_{uploaded_file.name.replace(' ', '_')}"
    file_path = UPLOAD_DIR / safe_name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ================= SAVE UPLOAD METADATA =================
    record_id = save_upload_metadata(
        filename=uploaded_file.name,
        filepath=str(file_path),
        content_type=uploaded_file.type,
        size_bytes=len(uploaded_file.getvalue()),
        uploaded_by="user"
    )

    st.session_state.record_id = record_id

    # ================= PDF METADATA =================
    if uploaded_file.type == "application/pdf":
        pdf_meta = extract_pdf_metadata(str(file_path))
        save_pdf_metadata(upload_id=record_id, metadata=pdf_meta)

    st.success(f"Document uploaded successfully (Record ID: {record_id})")

    # ================= RUN FORENSICS =================
    try:
        subprocess.run(
            ["python", str(DETAILS_SCRIPT)],
            check=True
        )

        subprocess.run(
            ["python", str(FORENCIS_SCRIPT)],
            check=True
        )

        st.success("Forensic processing completed")

    except Exception as e:
        st.error(f"Forensic analysis failed: {e}")
        st.stop()

    # ================= RUN SCORING =================
    st.write("Starting scoring...")
    scoring_result = run_scoring(record_id)

    st.session_state.scoring_result = scoring_result
    st.success("Scoring completed")

# ================= RESULTS CARD =================

# ================= RESULTS DASHBOARD =================

result = st.session_state.get("scoring_result")

if result:
    risk = float(result.get("risk_score", 0))
    verdict = result.get("verdict", "Unknown")
    ela = round(float(result.get("ela_score", 0)), 2)
    record_id = result.get("record_id")

    # -------- COLOR LOGIC --------
    if risk < 30:
        risk_color = "🟢 LOW RISK"
    elif risk < 60:
        risk_color = "🟠 MEDIUM RISK"
    else:
        risk_color = "🔴 HIGH RISK"

    st.subheader("Forensic Risk Assessment")

    # -------- FLASH CARDS --------
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Risk Score",
        f"{risk}%",
        help="Overall forensic manipulation probability"
    )

    col2.metric(
        "Verdict",
        verdict,
        help="Final decision based on combined forensic signals"
    )

    col3.metric(
        "Risk Level",
        risk_color,
        help="Categorized risk band"
    )

    st.markdown("---")

    # -------- LAYOUT: GRAPH + DETAILS --------
    left, right = st.columns([1, 2])

    with left:
        st.markdown("### Signal Snapshot")

        import pandas as pd
        import matplotlib.pyplot as plt

        df = pd.DataFrame({
            "Metric": ["Risk", "ELA"],
            "Score": [risk, ela * 10]
        })

        fig, ax = plt.subplots(figsize=(3, 2))
        bars = ax.bar(
            df["Metric"],
            df["Score"],
            color=["#d32f2f" if risk > 60 else "#f9a825" if risk > 30 else "#2e7d32",
                   "#1976d2"]
        )

        ax.set_ylim(0, 100)
        ax.set_title("Forensic Signals", fontsize=10)
        ax.tick_params(labelsize=8)

        st.pyplot(fig)

    with right:
        st.markdown("### Assessment Summary")
        st.write(
            f"""
            • **Risk Score:** {risk}%  
            • **ELA Signal Strength:** {ela}  
            • **Final Verdict:** {verdict}  

            This assessment is generated using multiple
            forensic techniques including compression analysis,
            error-level analysis (ELA), and noise inconsistencies.
            """
        )

    st.markdown("---")

    # -------- DOWNLOAD REPORT --------
    from pathlib import Path

    REPORTS_DIR = Path("reports")
    report_file = REPORTS_DIR / f"{record_id}_final_report.json"

    if report_file.exists():
        with open(report_file, "rb") as f:
            st.download_button(
                "⬇️ Download Forensic Report",
                data=f,
                file_name=report_file.name,
                mime="application/json"
            )
    else:
        st.info("Forensic report will be available after full processing.")

# ================= FOOTER =================
st.markdown("---")
st.caption("© 2025 Standard Chartered · Internal Prototype")
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

# ================= RESULTS CARD =================

result = st.session_state.get("scoring_result")

if result:
    st.subheader("Forensic Risk Assessment")

    risk = float(result.get("risk_score", 0))
    verdict = result.get("verdict", "Unknown")
    ela = round(float(result.get("ela_score", 0)), 2)
    report_path = result.get("report_path")

    # ---- METRICS ----
    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="Risk Score (%)",
        value=f"{risk}%",
        delta=None
    )

    col2.metric(
        label="Verdict",
        value=verdict
    )

    col3.metric(
        label="ELA Signal",
        value=ela
    )

    st.markdown("---")

    # ================= RISK DISTRIBUTION GRAPH =================
    st.subheader("Risk Assessment Distribution")

    import pandas as pd
    import matplotlib.pyplot as plt

    risk_data = pd.DataFrame({
        "Metric": ["Risk Score", "ELA Signal", "Remaining Margin"],
        "Value": [risk, ela * 10, max(0, 100 - risk)]
    })

    fig, ax = plt.subplots(figsize=(4,3))
    bars = ax.bar(
        risk_data["Metric"],
        risk_data["Value"]
    )

    ax.set_ylim(0, 100)
    ax.set_ylabel("Score")
    ax.set_title("Forensic Signal Breakdown")

    st.pyplot(fig)

    # ================= DOWNLOAD =================
   # ================= DOWNLOAD =================
report_path = result.get("report_path")

if report_path:
    report_file = Path(report_path)

    if report_file.exists():
        with open(report_file, "rb") as f:
            st.download_button(
                label="⬇️ Download Forensic Report (JSON)",
                data=f,
                file_name=report_file.name,
                mime="application/json"
            )
    else:
        st.warning("Forensic report not found on disk.")
else:
    st.warning("Report path not available yet.")   mime="application/json"
            )

# ================= FOOTER =================
st.markdown("---")
st.caption("© 2025 Standard Chartered · Internal Prototype")
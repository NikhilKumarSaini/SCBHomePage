# ========================== ANALYZE DOCUMENT ==========================

if st.button("Analyze Document"):

    if not uploaded_file:
        st.error("Please upload a document first")
        st.stop()

    steps = [
        "Uploading document",
        "Validating file",
        "Saving to secure storage",
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

    # ========================== SAVE FILE ==========================

    timestamp = int(time.time())
    safe_name = f"{timestamp}_{uploaded_file.name.replace(' ', '_')}"
    file_path = UPLOAD_DIR / safe_name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ========================== SAVE METADATA ==========================

    record_id = save_upload_metadata(
        filename=uploaded_file.name,
        filepath=str(file_path),
        content_type=uploaded_file.type,
        size_bytes=len(uploaded_file.getvalue()),
        uploaded_by="user"
    )

    st.success(f"Document uploaded successfully (Record ID: {record_id})")

    # ========================== PDF METADATA ==========================

    pdf_meta = {}
    if uploaded_file.type == "application/pdf":
        pdf_meta = extract_pdf_metadata(str(file_path))
        save_pdf_metadata(upload_id=record_id, metadata=pdf_meta)

    # ========================== RUN FORENSICS ==========================

    try:
        subprocess.run(
            ["python", str(DETAILS_SCRIPT), str(file_path), str(record_id)],
            check=True
        )

        subprocess.run(
            ["python", str(FORENSICS_SCRIPT), str(file_path), str(record_id)],
            check=True
        )

        st.success("Forensic processing completed")

    except Exception as e:
        st.error(f"Forensic analysis failed: {e}")
        st.stop()

    # ========================== RUN SCORING ==========================

    st.write("Starting scoring...")

    forensics_output_dir = ANALYSIS_OUTPUT_ROOT / str(record_id)

    scoring_result = run_scoring(
        record_id,
        forensics_output_dir,
        pdf_meta
    )

    st.session_state.scoring_result = scoring_result
    st.success("Scoring completed")

# ========================== RESULTS CARD ==========================

result = st.session_state.get("scoring_result")

if result:
    risk_score = float(result.get("risk_score", 0))
    verdict = result.get("verdict", "Unknown")

    ela = round(float(result.get("ela_score", 0)), 2)
    noise = round(float(result.get("noise_score", 0)), 2)
    compression = round(float(result.get("compression_score", 0)), 2)
    font = round(float(result.get("font_score", 0)), 2)

    if risk_score < 30:
        color = "green"
        level = "LOW RISK"
    elif risk_score < 70:
        color = "orange"
        level = "MEDIUM RISK"
    else:
        color = "red"
        level = "HIGH RISK"

    st.markdown("---")
    st.markdown("## 📊 Forensic Risk Assessment")

    st.markdown(
        f"""
        <div style="padding:20px;border-radius:12px;border:2px solid {color};">
            <h2 style="color:{color};">Risk Score: {risk_score:.2f}</h2>
            <h3>{level}</h3>
            <p><b>Verdict:</b> {verdict}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🔍 Individual Forensic Signals")
    st.write(f"ELA Score: {ela}")
    st.write(f"Noise Score: {noise}")
    st.write(f"Compression Score: {compression}")
    st.write(f"Font Alignment Score: {font}")

    # ========================== DOWNLOAD REPORT ==========================

    report_path = Path("reports") / f"forensic_report_{record_id}.txt"

    with open(report_path, "w") as f:
        f.write(f"Record ID: {record_id}\n")
        f.write(f"Risk Score: {risk_score}\n")
        f.write(f"Verdict: {verdict}\n\n")
        f.write(f"ELA Score: {ela}\n")
        f.write(f"Noise Score: {noise}\n")
        f.write(f"Compression Score: {compression}\n")
        f.write(f"Font Alignment Score: {font}\n")

    with open(report_path, "rb") as f:
        st.download_button(
            label="📥 Download Forensic Report",
            data=f,
            file_name=report_path.name,
            mime="text/plain"
        )

# ========================== FOOTER ==========================

st.markdown("---")
st.markdown(
    "<center>ML Document Forensics System • Internal Risk Assessment Tool</center>",
    unsafe_allow_html=True
)
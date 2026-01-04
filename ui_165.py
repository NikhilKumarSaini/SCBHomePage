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
            ["python", str(FORENCICS_SCRIPT)],
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
result = st.session_state.get("scoring_result")

if result:
    risk_score = float(result.get("risk_score", 0))
    verdict = result.get("verdict", "Unknown")
    ela_score = round(float(result.get("ela_score", 0)), 2)
    noise_score = round(float(result.get("noise_score", 0)), 2)
    compression_score = round(float(result.get("compression_score", 0)), 2)

    if risk_score < 30:
        color = "green"
        level = "LOW RISK"
    elif risk_score < 60:
        color = "orange"
        level = "MEDIUM RISK"
    else:
        color = "red"
        level = "HIGH RISK"

    st.markdown("---")
    st.markdown("## 🔍 Analysis Result")

    st.markdown(
        f"""
        <div style="padding:20px;border-radius:10px;border:1px solid #ddd">
            <h2 style="color:{color};margin-bottom:0">Risk Score: {risk_score:.2f}</h2>
            <h4 style="color:{color};margin-top:5px">{level}</h4>
            <p><b>Verdict:</b> {verdict}</p>
            <hr>
            <p>ELA Score: {ela_score}</p>
            <p>Noise Score: {noise_score}</p>
            <p>Compression Score: {compression_score}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ================= DOWNLOAD REPORT =================
    report_data = json.dumps(result, indent=4)

    st.download_button(
        label="⬇ Download Forensic Report",
        data=report_data,
        file_name=f"forensic_report_{result.get('record_id','doc')}.json",
        mime="application/json"
    )

# ================= FOOTER =================
st.markdown("---")
st.markdown(
    "<center>ML Forensic Project • Secure Document Analysis</center>",
    unsafe_allow_html=True
)
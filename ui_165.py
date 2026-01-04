# ======================= ANALYZE DOCUMENT =======================

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

    # ======================= SAVE FILE =======================
    timestamp = int(time.time())
    safe_name = f"{timestamp}_{uploaded_file.name.replace(' ', '_')}"
    file_path = UPLOAD_DIR / safe_name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ======================= SAVE UPLOAD METADATA =======================
    record_id = save_upload_metadata(
        filename=uploaded_file.name,
        filepath=str(file_path),
        content_type=uploaded_file.type,
        size_bytes=len(uploaded_file.getvalue()),
        uploaded_by="user"
    )

    st.session_state.record_id = record_id

    # ======================= PDF METADATA =======================
    pdf_meta = {}
    if uploaded_file.type == "application/pdf":
        pdf_meta = extract_pdf_metadata(str(file_path))
        save_pdf_metadata(upload_id=record_id, metadata=pdf_meta)

    st.success(f"Document uploaded successfully (Record ID: {record_id})")

    # ======================= RUN FORENSICS =======================
    try:
        subprocess.run(
            ["python", str(DETAILS_SCRIPT)],
            check=True
        )

        subprocess.run(
            ["python", str(FORENCICS_SCRIPT)],
            check=True
        )

        st.success("Forensic processing completed")

    except Exception as e:
        st.error(f"Forensic analysis failed: {e}")
        st.stop()

    # ======================= RUN SCORING =======================
    st.write("Starting scoring...")

    from scoring.final_runner import run_scoring

    forensics_output_dir = FORENSICS_OUTPUT_DIR / safe_name.replace(".pdf", "")

    scoring_result = run_scoring(
        pdf_path=str(file_path),
        forensics_output_dir=str(forensics_output_dir),
        pdf_metadata=pdf_meta
    )

    st.session_state.scoring_result = scoring_result
    st.success("Scoring completed")

# ======================= RESULTS CARD =======================

result = st.session_state.get("scoring_result")

if result:
    st.markdown("---")
    st.markdown("## 🧠 Forensic Risk Assessment")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Risk Score",
            f"{result['final_score']} %",
        )

    with col2:
        st.metric(
            "Verdict",
            "Manipulated" if result["ml_label"] == 1 else "Clean"
        )

    with col3:
        st.metric(
            "ML Probability",
            result["ml_probability"]
        )

    st.markdown("### 🔍 Forensic Signals")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("ELA", round(result["ela_score"], 3))
    c2.metric("Noise", round(result["noise_score"], 3))
    c3.metric("Compression", round(result["compression_score"], 3))
    c4.metric("Metadata", round(result["metadata_score"], 3))
    c5.metric("Font Align", round(result["font_score"], 3))

    # ======================= DOWNLOAD REPORT =======================
    st.markdown("---")

    report_json = json.dumps(result, indent=4)

    st.download_button(
        label="⬇️ Download Forensic Report",
        data=report_json,
        file_name=f"{safe_name}_forensic_report.json",
        mime="application/json"
    )

# ======================= FOOTER =======================

st.markdown(
    """
    <hr>
    <center>
        <small>
            ML Forensic Risk Assessment System<br>
            © Standard Chartered – Internal Use Only
        </small>
    </center>
    """,
    unsafe_allow_html=True
)
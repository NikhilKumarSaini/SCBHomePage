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

result = st.session_state.get("scoring_result")

if result:
    st.subheader("Forensic Risk Assessment")

    risk = float(result.get("risk_score", 0))
    verdict = result.get("verdict", "Unknown")
    ela = round(float(result.get("ela_score", 0)), 2)
    confidence = float(result.get("confidence", 0.0))
    report_path = result.get("report_path")

    # Color logic (SCB style)
    risk_color = "#E5533D" if risk > 60 else "#F4B400" if risk > 30 else "#1DB954"
    verdict_color = "#1DB954" if verdict.lower() == "clean" else "#E5533D"

    st.markdown(
        f"""
        <div style="display:flex; gap:24px; margin-top:25px;">

            <div style="flex:1; background:#F5F9FF; padding:22px; border-radius:14px;
                        border-left:6px solid {risk_color}; box-shadow:0 4px 10px rgba(0,0,0,0.06)">
                <h4 style="margin-bottom:6px;">Risk Score</h4>
                <h1 style="color:{risk_color}; margin:0;">{risk}%</h1>
            </div>

            <div style="flex:1; background:#F5FFF8; padding:22px; border-radius:14px;
                        border-left:6px solid {verdict_color}; box-shadow:0 4px 10px rgba(0,0,0,0.06)">
                <h4 style="margin-bottom:6px;">Verdict</h4>
                <h1 style="color:{verdict_color}; margin:0;">{verdict}</h1>
            </div>

            <div style="flex:1; background:#FFF9F3; padding:22px; border-radius:14px;
                        border-left:6px solid #0033A0; box-shadow:0 4px 10px rgba(0,0,0,0.06)">
                <h4 style="margin-bottom:6px;">ELA Signal</h4>
                <h1 style="color:#0033A0; margin:0;">{ela}</h1>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ================= CONFIDENCE BAR =================

    st.markdown("### Analysis Confidence")
    st.progress(int(confidence * 100))
    st.caption(f"Confidence level: {int(confidence * 100)}%")

    # ================= DOWNLOAD REPORT =================

    if report_path and Path(report_path).exists():
        with open(report_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Forensic Report (JSON)",
                data=f,
                file_name=Path(report_path).name,
                mime="application/json"
            )

# ================= FOOTER =================

st.markdown(
    """
    <hr style="margin-top:40px;"/>
    <div style="text-align:center; color:#6b6b6b; font-size:14px;">
        © 2025 Standard Chartered · Internal Prototype
    </div>
    """,
    unsafe_allow_html=True
)
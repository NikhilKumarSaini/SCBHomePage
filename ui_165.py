# ====================== ANALYZE DOCUMENT ======================

if st.button("Analyze Document"):
    if not uploaded_file:
        st.error("Please upload a document first")
        st.stop()

    # ---------- Progress UI ----------
    steps = [
        "Uploading document",
        "Saving file",
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

    # ---------- SAVE FILE ----------
    timestamp = int(time.time())
    safe_name = f"{timestamp}_{uploaded_file.name.replace(' ', '_')}"
    file_path = UPLOAD_DIR / safe_name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Document uploaded successfully (Record ID: {timestamp})")

    # ---------- RUN FORENSICS ----------
    try:
        subprocess.run(
            ["python", str(FORENSICS_SCRIPT), str(file_path), str(timestamp)],
            check=True
        )
        st.success("Forensic processing completed")
    except Exception as e:
        st.error(f"Forensic analysis failed: {e}")
        st.stop()

    # ---------- RUN SCORING ----------
    st.write("Starting scoring...")
    try:
        scoring_result = run_scoring(
            record_id=timestamp,
            pdf_path=str(file_path)
        )
        st.session_state.scoring_result = scoring_result
        st.success("Scoring completed")
    except Exception as e:
        st.error(f"Scoring failed: {e}")
        st.stop()

# ====================== RESULTS CARD ======================

result = st.session_state.get("scoring_result")

if result:
    st.markdown("---")
    st.subheader("📊 Forensic Analysis Result")

    risk_score = float(result.get("ml_probability", 0))
    verdict = result.get("verdict", "Unknown")

    ela = round(float(result.get("ela_score", 0)), 2)
    noise = round(float(result.get("noise_score", 0)), 2)
    compression = round(float(result.get("compression_score", 0)), 2)
    font = round(float(result.get("font_score", 0)), 2)

    # ---------- Color Logic ----------
    if risk_score >= 0.7:
        color = "🔴"
    elif risk_score >= 0.4:
        color = "🟠"
    else:
        color = "🟢"

    # ---------- Summary ----------
    st.markdown(
        f"""
        ### {color} Verdict: **{verdict}**

        **Manipulation Probability:** `{round(risk_score, 3)}`

        ---
        **Forensic Scores**
        - ELA Score: `{ela}`
        - Noise Score: `{noise}`
        - Compression Score: `{compression}`
        - Font Alignment Score: `{font}`
        """
    )

    # ---------- DOWNLOAD REPORT ----------
    report_text = f"""
ML Forensic Analysis Report
--------------------------
Record ID: {result.get('record_id')}

Verdict: {verdict}
Manipulation Probability: {risk_score}

ELA Score: {ela}
Noise Score: {noise}
Compression Score: {compression}
Font Alignment Score: {font}
"""

    st.download_button(
        label="📥 Download Report",
        data=report_text,
        file_name=f"forensic_report_{result.get('record_id')}.txt",
        mime="text/plain"
    )

# ====================== FOOTER ======================

st.markdown("---")
st.caption("ML Forensic Project • Internal Use Only")
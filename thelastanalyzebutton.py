# ------------------------------------------------------------------
# ANALYZE BUTTON
# ------------------------------------------------------------------
if st.button("Analyze Document"):
    if not uploaded_file:
        st.error("Please upload a valid document first")
    else:
        with st.spinner("Running forensic analysis... Please wait"):

            # ----------------------------------------------------------
            # SAVE FILE WITH UNIX TIMESTAMP
            # ----------------------------------------------------------
            unix_ts = int(time.time())
            safe_name = f"{unix_ts}_{uploaded_file.name}"
            file_path = UPLOAD_DIR / safe_name

            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            # ----------------------------------------------------------
            # DB: SAVE UPLOAD METADATA
            # ----------------------------------------------------------
            record_id = save_upload_metadata(
                filename=safe_name,
                filepath=str(file_path),
                content_type=uploaded_file.type,
                size_bytes=uploaded_file.size
            )

            # ----------------------------------------------------------
            # PDF METADATA
            # ----------------------------------------------------------
            if uploaded_file.type == "application/pdf":
                metadata = extract_pdf_metadata(str(file_path))
                save_pdf_metadata(record_id, metadata)

            # ----------------------------------------------------------
            # SOURCECODE PIPELINE (UNCHANGED)
            # ----------------------------------------------------------
            subprocess.run(["python", str(DETAILS_SCRIPT)], check=True)
            subprocess.run(["python", str(FORENSICS_SCRIPT)], check=True)

            # ----------------------------------------------------------
            # SCORING + ML
            # ----------------------------------------------------------
            final_report = run_scoring(
                record_id=record_id,
                pdf_path=str(file_path)
            )

            # -------- STORE RESULT IN SESSION (KEY FIX) --------
            st.session_state.final_report = final_report
            st.session_state.analysis_done = True

        st.success("Analysis completed successfully!")

# ==========================================================
# RESULTS DASHBOARD (SESSION SAFE)
# ==========================================================
if st.session_state.analysis_done:

    final_report = st.session_state.final_report

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
    # ✅ SINGLE PDF RISK GRAPH (FIXED)
    # ------------------------------
    st.markdown("### 📈 Uploaded Document Risk")

    st.bar_chart(
        {
            "Risk Score": [final_score]
        },
        height=180
    )

    # ------------------------------
    # TECHNICAL DETAILS
    # ------------------------------
    with st.expander("🔍 View Detailed Technical Report"):
        st.json(final_report)

    # ------------------------------
    # DOWNLOAD BUTTONS (NO RESET)
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

    # ---- Download Forensics ZIP (MEMORY SAFE)
    forensics_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(report_path),
            "..",
            "Forensics_Output",
            final_report["forensics_folder"]
        )
    )

    if st.session_state.forensics_zip is None and os.path.exists(forensics_dir):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(forensics_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, forensics_dir)
                    zipf.write(file_path, arcname)
        zip_buffer.seek(0)
        st.session_state.forensics_zip = zip_buffer

    if st.session_state.forensics_zip:
        with c2:
            st.download_button(
                label="⬇ Download Forensics Evidence (ZIP)",
                data=st.session_state.forensics_zip,
                file_name=f"{final_report['forensics_folder']}.zip",
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
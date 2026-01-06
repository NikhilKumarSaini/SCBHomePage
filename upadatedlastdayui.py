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
        # MINI GRAPH: VERDICT vs SCORE
        # ------------------------------
        st.markdown("### 📈 Risk Overview")

        verdict_labels = [
            "Clean", "Negligible", "Low", "Moderate",
            "High", "Very High", "Critical"
        ]
        verdict_thresholds = [0, 10, 35, 55, 75, 90, 100]

        chart_data = {
            "Risk Level": verdict_labels,
            "Threshold Score": verdict_thresholds
        }

        st.bar_chart(chart_data, x="Risk Level", y="Threshold Score", height=220)

        # ------------------------------
        # TECHNICAL DETAILS
        # ------------------------------
        with st.expander("🔍 View Detailed Technical Report"):
            st.json(final_report)

        # ------------------------------
        # DOWNLOAD BUTTONS
        # ------------------------------
        c1, c2 = st.columns(2)

        # Download JSON Report
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

        # Download Forensics Output (ZIP)
        forensics_dir = os.path.join(
            os.path.dirname(report_path),
            "..",
            "Forensics_Output",
            final_report["forensics_folder"]
        )
        forensics_dir = os.path.abspath(forensics_dir)

        if os.path.exists(forensics_dir):
            with c2:
                zip_path = f"{forensics_dir}.zip"
                shutil.make_archive(forensics_dir, 'zip', forensics_dir)

                with open(zip_path, "rb") as z:
                    st.download_button(
                        label="⬇ Download Forensics Evidence (ZIP)",
                        data=z,
                        file_name=os.path.basename(zip_path),
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
# ==========================================================
        # RESULTS SECTION (FINAL – SINGLE SCORE)
        # ==========================================================
        st.markdown("## 📊 Risk Assessment Result")

        final_result = final_report["final_result"]

        final_score = final_result["final_score"]
        risk_category = final_result["risk_category"]

        # ------------------------------
        # FLASH CARDS
        # ------------------------------
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #0033A0, #0075B7);
                    padding: 30px;
                    border-radius: 14px;
                    color: white;
                    box-shadow: 0 10px 24px rgba(0,0,0,0.15);
                ">
                    <h2 style="margin-bottom: 8px;">Final Risk Score</h2>
                    <h1 style="font-size: 48px; margin: 0;">
                        {final_score} / 100
                    </h1>
                    <p style="margin-top: 10px; font-size: 16px;">
                        Risk Category: <b>{risk_category}</b>
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            # Small bar-style visualization
            st.markdown("#### Risk Level")
            st.progress(min(final_score / 100, 1.0))

            st.caption(
                "Scale: 0 (No Risk) → 100 (Critical Risk)"
            )

        # ------------------------------
        # OPTIONAL DETAILS (EXPANDER)
        # ------------------------------
        with st.expander("🔍 View Detailed Technical Report"):
            st.json(final_report)

        # ------------------------------
        # DOWNLOAD REPORT
        # ------------------------------
        report_path = final_report.get("report_path")

        if report_path and os.path.exists(report_path):
            with open(report_path, "rb") as f:
                st.download_button(
                    label="⬇ Download Full JSON Report",
                    data=f,
                    file_name=os.path.basename(report_path),
                    mime="application/json"
                )

# ------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------
st.markdown("""
<footer>
AI-Powered Document Forensics System · Built for Secure Financial Integrity Analysis
</footer>
""", unsafe_allow_html=True)
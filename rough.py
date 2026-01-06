import time
import shutil
import io
import zipfile

# ---------------- SESSION STATE INIT ----------------
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "final_report" not in st.session_state:
    st.session_state.final_report = None

if "forensics_zip" not in st.session_state:
    st.session_state.forensics_zip = None
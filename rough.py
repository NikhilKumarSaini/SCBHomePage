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


You are a Python Backend Developer.

I am working with a set of SAP HANA artifacts, including ".hdbcalculationview", ".hdbtable", ".hdbprocedure", and ".hdbfunction" files, organized in a directory.

I need to build a Python-based parser that:

- Reads all files from the given directory
- Identifies ".hdbcalculationview" files (XML format)
- Parses each file and extracts:
  - DataSources (table references from <DataSource id="...">)
  - View Attributes (column names from <viewAttribute id="...">)

Output Requirements:

- Structure the extracted data in clean JSON format
- Include the file name (view name), list of tables, and attributes
- Print readable output in the console

Code Requirements:

- Keep the implementation simple and beginner-friendly
- Add clear comments explaining each step
- Use standard Python libraries where possible
- Handle multiple files efficiently
- Include basic error handling (invalid XML, missing tags)

Design Requirement:

- Write the code in a modular way so it can be extended later to support ".hdbtable" and ".hdbprocedure" parsing

Also provide:

- Step-by-step instructions to run the script
- Any dependencies (if required)
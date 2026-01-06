with c2:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(forensics_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, forensics_dir)
                zipf.write(file_path, arcname)

    zip_buffer.seek(0)

    st.download_button(
        label="⬇ Download Forensics Evidence (ZIP)",
        data=zip_buffer,
        file_name=f"{final_report['forensics_folder']}.zip",
        mime="application/zip"
    )
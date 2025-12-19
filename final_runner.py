import os
import json
from db_utils import fetch_upload
from utils.pdf_metadata import get_pdf_metadata

from scoring.ela_score import calculate_ela_score
from scoring.metadata_score import calculate_metadata_score
from scoring.final_score import calculate_final_risk


def run_scoring(upload_id: int) -> dict:
    """
    Main scoring entrypoint using DB upload_id
    """

    # 1️⃣ Fetch upload details from DB
    upload = fetch_upload(upload_id)
    if not upload:
        raise ValueError("Invalid upload_id")

    filename = upload["filename"]
    filepath = upload["filepath"]

    # 2️⃣ Locate forensic output folder
    forensic_dir = None
    for d in os.listdir("Forensics_Output"):
        if filename.replace(" ", "_") in d:
            forensic_dir = os.path.join("Forensics_Output", d)
            break

    if not forensic_dir:
        raise FileNotFoundError("Forensic output not found")

    # 3️⃣ Locate ELA image
    ela_image = os.path.join(forensic_dir, "ELA", "page-1.jpg")

    # 4️⃣ Read PDF metadata
    pdf_metadata = get_pdf_metadata(filepath)

    # 5️⃣ Calculate individual scores
    ela_score = calculate_ela_score(ela_image)
    metadata_score = calculate_metadata_score(pdf_metadata)

    # placeholders (already processed by your pipeline)
    compression_score = 0.5
    ocr_score = 0.3

    # 6️⃣ Final risk calculation
    final = calculate_final_risk(
        ela_score,
        compression_score,
        ocr_score,
        metadata_score
    )

    result = {
        "upload_id": upload_id,
        "filename": filename,
        "ela_score": ela_score,
        "metadata_score": metadata_score,
        "compression_score": compression_score,
        "ocr_score": ocr_score,
        **final
    }

    os.makedirs("reports", exist_ok=True)
    with open(f"reports/{upload_id}_final_report.json", "w") as f:
        json.dump(result, f, indent=4)

    return result
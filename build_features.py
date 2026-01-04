import json
import csv
from pathlib import Path

REPORTS_DIR = Path("reports")
OUT_CSV = Path("ml/ml_features.csv")

fields = [
    "ela_score",
    "noise_score",
    "compression_score",
    "font_alignment_score",
    "metadata_score",
    "label"   # 1 = fake, 0 = real
]

rows = []

for report in REPORTS_DIR.glob("*_final_report.json"):
    with open(report) as f:
        data = json.load(f)

    s = data["scoring"]

    row = {
        "ela_score": s["ela_score"],
        "noise_score": s["noise_score"],
        "compression_score": s["compression_score"],
        "font_alignment_score": s["font_alignment_score"],
        "metadata_score": s["metadata_score"],
        "label": int(input(f"Is {data['file_name']} FAKE? (1=yes, 0=no): "))
    }

    rows.append(row)

with open(OUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print("ml_features.csv created")
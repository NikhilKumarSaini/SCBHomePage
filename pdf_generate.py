from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import os
from datetime import datetime

OUTPUT_DIR = "sample_statements"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PAGE_W, PAGE_H = A4


# -------------------------------------------------
# COMMON STATEMENT CONTENT
# -------------------------------------------------
def draw_statement_text(c, closing_balance):
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, "STANDARD BANK OF INDIA")

    c.setFont("Helvetica", 10)
    c.drawString(50, 775, "Account Holder : Rahul Sharma")
    c.drawString(50, 760, "Account Number : XXXX-4589")
    c.drawString(50, 745, "Statement Period : 01 Jan 2024 – 31 Jan 2024")

    c.line(50, 735, 545, 735)

    c.drawString(50, 715, "Date")
    c.drawString(120, 715, "Description")
    c.drawString(340, 715, "Debit")
    c.drawString(420, 715, "Credit")
    c.drawString(500, 715, "Balance")

    y = 690
    rows = [
        ("01-01-24", "Opening Balance", "", "", "20,000"),
        ("05-01-24", "Salary Credit", "", "50,000", "70,000"),
        ("10-01-24", "ATM Withdrawal", "5,000", "", "65,000"),
        ("15-01-24", "UPI Transfer", "2,000", "", "63,000"),
        ("20-01-24", "Online Purchase", "3,000", "", "60,000"),
    ]

    for row in rows:
        c.drawString(50, y, row[0])
        c.drawString(120, y, row[1])
        c.drawString(340, y, row[2])
        c.drawString(420, y, row[3])
        c.drawString(500, y, row[4])
        y -= 20

    c.line(50, y, 545, y)
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(340, y, "Closing Balance")
    c.drawString(500, y, closing_balance)

    c.setFont("Helvetica", 9)
    c.drawString(50, 100, "This is a system generated statement.")
    c.drawString(50, 85, f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}")

# -------------------------------------------------
# 1️⃣ CLEAN STATEMENT
# -------------------------------------------------
def generate_clean_pdf():
    path = f"{OUTPUT_DIR}/statement_clean.pdf"
    c = canvas.Canvas(path, pagesize=A4)
    draw_statement_text(c, "60,000")
    c.save()
    print("✅ Clean statement generated")

# -------------------------------------------------
# 2️⃣ MANIPULATED – IMAGE EDIT + RECOMPRESSION
# -------------------------------------------------
def generate_manipulated_edit():
    img = Image.new("RGB", (595, 842), "white")
    d = ImageDraw.Draw(img)

    # Draw full statement as image
    d.text((50, 40), "STANDARD BANK OF INDIA", fill="black")
    d.text((50, 80), "Account Holder : Rahul Sharma", fill="black")
    d.text((50, 100), "Account Number : XXXX-4589", fill="black")
    d.text((50, 120), "Statement Period : 01 Jan 2024 – 31 Jan 2024", fill="black")

    d.text((50, 180), "Closing Balance", fill="black")

    # FAKE EDIT REGION (classic fraud)
    d.rectangle([230, 170, 360, 210], fill="white")
    d.text((240, 180), "9,60,000", fill="black")  # manipulated balance

    # Save with heavy JPEG compression
    img_path = f"{OUTPUT_DIR}/temp_edit.jpg"
    img.save(img_path, "JPEG", quality=35)

    c = canvas.Canvas(f"{OUTPUT_DIR}/statement_manipulated_edit.pdf", pagesize=A4)
    c.drawImage(img_path, 0, 0, width=PAGE_W, height=PAGE_H)
    c.save()
    print("⚠️ Manipulated (edit) statement generated")

# -------------------------------------------------
# 3️⃣ MANIPULATED – NOISE + MULTI SAVE
# -------------------------------------------------
def generate_manipulated_noise():
    img = np.ones((842, 595, 3), dtype=np.uint8) * 255

    cv2.putText(img, "STANDARD BANK OF INDIA", (50, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.putText(img, "Closing Balance : 7,40,000", (50, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

    # Add Gaussian noise (scanner-like)
    noise = np.random.normal(0, 18, img.shape).astype(np.uint8)
    noisy = cv2.add(img, noise)

    img_path = f"{OUTPUT_DIR}/temp_noise.jpg"
    cv2.imwrite(img_path, noisy, [cv2.IMWRITE_JPEG_QUALITY, 40])

    c = canvas.Canvas(f"{OUTPUT_DIR}/statement_manipulated_noise.pdf", pagesize=A4)
    c.drawImage(img_path, 0, 0, width=PAGE_W, height=PAGE_H)
    c.save()
    print("⚠️ Manipulated (noise) statement generated")

# -------------------------------------------------
# RUN ALL
# -------------------------------------------------
generate_clean_pdf()
generate_manipulated_edit()
generate_manipulated_noise()

print("\n📂 Files generated in folder: sample_statements/")

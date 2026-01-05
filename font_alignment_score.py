import os
import numpy as np
from PIL import Image


def compute_font_alignment_score(forensic_output_dir: str) -> float:
    font_dir = os.path.join(forensic_output_dir, "Font_Alignment")

    if not os.path.exists(font_dir):
        return 0.0

    scores = []
    for img in os.listdir(font_dir):
        if img.lower().endswith(".jpg"):
            img_path = os.path.join(font_dir, img)
            image = Image.open(img_path).convert("L")
            scores.append(np.array(image).std())

    return round(float(np.mean(scores)) / 255, 3) if scores else 0.0
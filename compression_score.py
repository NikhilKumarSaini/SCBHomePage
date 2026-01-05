import os
from PIL import Image
import numpy as np


def compute_compression_score(forensic_output_dir: str) -> float:
    comp_dir = os.path.join(forensic_output_dir, "Compression")

    if not os.path.exists(comp_dir):
        return 0.0

    scores = []
    for img in os.listdir(comp_dir):
        if img.lower().endswith(".jpg"):
            img_path = os.path.join(comp_dir, img)
            image = Image.open(img_path).convert("RGB")
            scores.append(np.array(image).std())

    return round(float(np.mean(scores)) / 255, 3) if scores else 0.0
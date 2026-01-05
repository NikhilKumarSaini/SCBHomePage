import os
from PIL import Image
import numpy as np


def compute_ela_score(forensic_output_dir: str) -> float:
    ela_dir = os.path.join(forensic_output_dir, "ELA")

    if not os.path.exists(ela_dir):
        return 0.0

    scores = []
    for img in os.listdir(ela_dir):
        if img.lower().endswith(".jpg"):
            img_path = os.path.join(ela_dir, img)
            image = Image.open(img_path).convert("RGB")
            arr = np.array(image)
            scores.append(arr.std())

    return round(float(np.mean(scores)) / 255, 3) if scores else 0.0
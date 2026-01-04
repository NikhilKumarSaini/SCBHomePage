import os
import numpy as np
from PIL import Image

def compute_font_alignment_score(alignment_image_path: str) -> float:
    """
    Converts font alignment visual inconsistencies into risk score (0–1)
    """

    if not os.path.exists(alignment_image_path):
        return 0.0  # no anomaly detected

    img = Image.open(alignment_image_path).convert("L")
    arr = np.array(img)

    # Measure vertical variance (misalignment)
    vertical_variance = np.var(arr.mean(axis=1))

    # Normalize (empirical thresholds)
    if vertical_variance < 20:
        score = 0.1
    elif vertical_variance < 50:
        score = 0.3
    elif vertical_variance < 100:
        score = 0.6
    else:
        score = 0.9

    return round(score, 4)
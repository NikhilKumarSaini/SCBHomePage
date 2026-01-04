import cv2
import numpy as np
import math
import tempfile
import os
from SourceCode.compression import detect_compression  # existing code

def _entropy(img):
    hist = cv2.calcHist([img], [0], None, [256], [0,256])
    hist = hist / hist.sum()
    return -np.sum([p * math.log2(p) for p in hist if p > 0])

def compute_compression_score(image_path: str) -> float:
    """
    Converts compression artifacts into a normalized score (0–1)
    """

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        compression_output = tmp.name

    try:
        # run existing compression detection (UNCHANGED)
        detect_compression(
            image_path=image_path,
            save_path=compression_output
        )

        img = cv2.imread(compression_output, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return 0.0

        entropy_val = _entropy(img)

        # normalize entropy
        # clean docs ~ 4–5, manipulated ~ 6–7+
        score = min(max((entropy_val - 4.5) / 2.5, 0), 1)

        return round(float(score), 4)

    finally:
        if os.path.exists(compression_output):
            os.remove(compression_output)
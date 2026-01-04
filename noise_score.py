import cv2
import numpy as np
import os
import tempfile
from SourceCode.noise import detect_noise  # existing code

def compute_noise_score(image_path: str) -> float:
    """
    Runs noise detection and converts output to a normalized score (0–1).
    """

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        noise_output_path = tmp.name

    try:
        # run existing noise detection (UNCHANGED)
        detect_noise(
            image_path=image_path,
            save_path=noise_output_path
        )

        # load noise image
        img = cv2.imread(noise_output_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return 0.0

        # compute noise variance
        noise_std = np.std(img)

        # normalize (empirically capped)
        noise_score = min(noise_std / 50.0, 1.0)

        return round(float(noise_score), 4)

    finally:
        if os.path.exists(noise_output_path):
            os.remove(noise_output_path)
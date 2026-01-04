from pathlib import Path
import cv2
import numpy as np

from SourceCode.noise import noise_pattern_analysis


def compute_noise_score(image_path: str) -> float:
    """
    Computes noise score (0–1) using teammate's noise_pattern_analysis
    """

    image_path = Path(image_path)

    # temp output path (noise image)
    temp_noise_path = image_path.parent / "_noise_tmp.jpg"

    # run teammate logic (creates noise visualization)
    noise_pattern_analysis(str(image_path), str(temp_noise_path))

    # read generated noise image
    noise_img = cv2.imread(str(temp_noise_path), cv2.IMREAD_GRAYSCALE)

    if noise_img is None:
        return 0.0

    # ---- SCORE LOGIC ----
    # High variance = more manipulation artifacts
    variance = float(np.var(noise_img))

    # normalize variance → 0–1
    score = min(variance / 5000.0, 1.0)

    # cleanup
    try:
        temp_noise_path.unlink()
    except Exception:
        pass

    return round(score, 3)
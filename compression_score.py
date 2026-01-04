from pathlib import Path
import cv2
import numpy as np

from SourceCode.compression import compression_difference


def compute_compression_score(image_path: str) -> float:
    """
    Computes compression artifact score (0–1)
    using teammate's compression_difference
    """

    image_path = Path(image_path)

    # temp output path
    temp_comp_path = image_path.parent / "_compression_tmp.jpg"

    # run teammate function (creates diff image)
    compression_difference(str(image_path), str(temp_comp_path))

    # read compression diff image
    comp_img = cv2.imread(str(temp_comp_path), cv2.IMREAD_GRAYSCALE)

    if comp_img is None:
        return 0.0

    # ---- SCORE LOGIC ----
    # higher contrast differences = more tampering
    mean_intensity = float(np.mean(comp_img))

    # normalize → 0–1
    score = min(mean_intensity / 255.0, 1.0)

    # cleanup
    try:
        temp_comp_path.unlink()
    except Exception:
        pass

    return round(score, 3)
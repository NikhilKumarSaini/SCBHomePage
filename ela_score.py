import numpy as np
from PIL import Image
from SourceCode.ela import perform_ela
import os
import tempfile

def compute_ela_score(image_path: str) -> float:
    """
    Runs ELA using existing code and computes a normalized ELA score.
    Returns value between 0 and 1.
    """

    # create temp file for ELA output
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        ela_output_path = tmp.name

    try:
        # run existing ELA (UNCHANGED)
        perform_ela(
            image_path=image_path,
            save_path=ela_output_path,
            quality=90
        )

        # load ELA image
        ela_img = Image.open(ela_output_path).convert("L")
        ela_array = np.array(ela_img, dtype=np.float32)

        # mean intensity
        mean_intensity = np.mean(ela_array)

        # normalize (0–255 → 0–1)
        ela_score = mean_intensity / 255.0

        return round(float(ela_score), 4)

    finally:
        if os.path.exists(ela_output_path):
            os.remove(ela_output_path)
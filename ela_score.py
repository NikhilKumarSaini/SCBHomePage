import cv2
import numpy as np
import os

def calculate_ela_score(ela_image_path: str) -> float:
    """
    Calculates ELA inconsistency score based on pixel intensity variance
    Returns value between 0.0 – 0.7
    """
    if not os.path.exists(ela_image_path):
        return 0.0

    img = cv2.imread(ela_image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0.0

    mean_intensity = np.mean(img)

    if mean_intensity < 10:
        return 0.1
    elif mean_intensity < 20:
        return 0.4
    else:
        return 0.7
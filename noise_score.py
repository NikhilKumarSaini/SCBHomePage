import os
import cv2
import numpy as np


def compute_noise_score(forensic_output_dir: str) -> float:
    noise_dir = os.path.join(forensic_output_dir, "Noise")

    if not os.path.exists(noise_dir):
        return 0.0

    scores = []
    for img in os.listdir(noise_dir):
        if img.lower().endswith(".jpg"):
            img_path = os.path.join(noise_dir, img)
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            scores.append(image.std())

    return round(float(np.mean(scores)) / 255, 3) if scores else 0.0
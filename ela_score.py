import cv2
import numpy as np
import os

def compute_ela_score(ela_dir):
    if not os.path.exists(ela_dir):
        return 0

    scores = []

    for img in os.listdir(ela_dir):
        if not img.lower().endswith(".jpg"):
            continue

        path = os.path.join(ela_dir, img)
        im = cv2.imread(path)

        if im is None:
            continue

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        variance = np.var(gray)

        scores.append(variance)

    if not scores:
        return 0

    avg_var = np.mean(scores)

    # Normalize → higher variance = more manipulation
    ela_score = min(100, avg_var / 5)

    return round(float(ela_score), 2)
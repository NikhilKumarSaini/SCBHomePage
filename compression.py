import cv2
import numpy as np
import os

def compute_compression_score(comp_dir):
    if not os.path.exists(comp_dir):
        return 0

    diffs = []

    for img in os.listdir(comp_dir):
        if not img.lower().endswith(".jpg"):
            continue

        path = os.path.join(comp_dir, img)
        im = cv2.imread(path)

        if im is None:
            continue

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        diffs.append(np.var(lap))

    if not diffs:
        return 0

    avg = np.mean(diffs)

    comp_score = min(100, avg / 10)

    return round(float(comp_score), 2)
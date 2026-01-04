import cv2
import numpy as np
import os

def compute_font_alignment_score(font_dir):
    if not os.path.exists(font_dir):
        return 0

    heat_vals = []

    for img in os.listdir(font_dir):
        if not img.lower().endswith(".jpg"):
            continue

        path = os.path.join(font_dir, img)
        im = cv2.imread(path)

        if im is None:
            continue

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        heat_vals.append(np.std(gray))

    if not heat_vals:
        return 0

    avg_dev = np.mean(heat_vals)

    font_score = min(100, avg_dev * 2)

    return round(float(font_score), 2)
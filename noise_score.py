import cv2
import numpy as np
import os

def compute_noise_score(noise_dir):
    if not os.path.exists(noise_dir):
        return 0

    values = []

    for img in os.listdir(noise_dir):
        if not img.lower().endswith(".jpg"):
            continue

        path = os.path.join(noise_dir, img)
        im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        if im is None:
            continue

        std = np.std(im)
        values.append(std)

    if not values:
        return 0

    avg_noise = np.mean(values)

    noise_score = min(100, avg_noise * 1.5)

    return round(float(noise_score), 2)
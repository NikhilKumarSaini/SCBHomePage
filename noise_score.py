import os

def compute_noise_score(forensic_dir: str) -> float:
    noise_dir = os.path.join(forensic_dir, "Noise")
    if not os.path.exists(noise_dir):
        return 0.0

    images = [f for f in os.listdir(noise_dir) if f.lower().endswith(".jpg")]
    return min(100.0, len(images) * 20.0)
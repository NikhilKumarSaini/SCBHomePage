import os

def compute_compression_score(forensic_dir: str) -> float:
    comp_dir = os.path.join(forensic_dir, "Compression")
    if not os.path.exists(comp_dir):
        return 0.0

    images = [f for f in os.listdir(comp_dir) if f.lower().endswith(".jpg")]
    return min(100.0, len(images) * 20.0)
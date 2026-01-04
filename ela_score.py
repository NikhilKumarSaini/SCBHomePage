import os

def compute_ela_score(forensic_dir: str) -> float:
    ela_dir = os.path.join(forensic_dir, "ELA")
    if not os.path.exists(ela_dir):
        return 0.0

    images = [f for f in os.listdir(ela_dir) if f.lower().endswith(".jpg")]
    if not images:
        return 0.0

    # Simple heuristic
    return min(100.0, len(images) * 20.0)
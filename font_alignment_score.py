import os

def compute_font_alignment_score(forensic_dir: str) -> float:
    font_dir = os.path.join(forensic_dir, "Font_Alignment")
    if not os.path.exists(font_dir):
        return 0.0

    images = [f for f in os.listdir(font_dir) if f.lower().endswith(".jpg")]
    return min(100.0, len(images) * 25.0)
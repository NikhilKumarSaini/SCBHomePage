from PIL import Image, ImageChops
import os


def run_compression_forensics(
    image_path: str,
    upload_id: int,
    forensics_root: str = "outputs/forensics"
):
    """
    Perform JPEG compression difference analysis on a single image.

    Args:
        image_path (str): Path to input image (PDF page image)
        upload_id (int): Upload record ID (used for folder isolation)
        forensics_root (str): Root forensic output folder

    Returns:
        str: Path to compression difference image
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Create upload-specific compression folder
    compression_dir = os.path.join(
        forensics_root,
        f"upload_{upload_id}",
        "Compression"
    )
    os.makedirs(compression_dir, exist_ok=True)

    # Load image
    img = Image.open(image_path).convert("RGB")
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    # Temp paths
    low_path = os.path.join(compression_dir, f"{base_name}_low.jpg")
    high_path = os.path.join(compression_dir, f"{base_name}_high.jpg")

    # Final output
    diff_path = os.path.join(
        compression_dir,
        f"{base_name}_compression_diff.jpg"
    )

    # Save compressed versions
    img.save(low_path, "JPEG", quality=70)
    img.save(high_path, "JPEG", quality=95)

    # Compute difference
    low_img = Image.open(low_path)
    high_img = Image.open(high_path)

    diff = ImageChops.difference(low_img, high_img)
    diff.save(diff_path)

    # Cleanup temp files
    low_img.close()
    high_img.close()
    os.remove(low_path)
    os.remove(high_path)

    print(f"[Compression] Generated: {diff_path}")
    return diff_path
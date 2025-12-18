import fitz  # PyMuPDF
import os


def convert_pdf_to_images(pdf_path: str, outputs_base_dir: str):
    """
    Convert a single PDF into images (one folder per PDF)

    Args:
        pdf_path (str): Full path of uploaded PDF (from uploads/)
        outputs_base_dir (str): Base outputs folder (e.g. outputs/images)

    Returns:
        output_folder (str): Folder where images are saved
    """

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Ensure outputs base directory exists
    os.makedirs(outputs_base_dir, exist_ok=True)

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(outputs_base_dir, pdf_name)
    os.makedirs(output_folder, exist_ok=True)

    print(f"Converting PDF: {pdf_name}")
    doc = None

    try:
        doc = fitz.open(pdf_path)

        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)
            pix = page.get_pixmap()

            image_name = f"page_{page_number + 1}.jpg"
            image_path = os.path.join(output_folder, image_name)

            pix.save(image_path)

        print(f"Converted {doc.page_count} pages successfully")

    except Exception as e:
        print(f"Error converting PDF {pdf_name}: {str(e)}")
        raise

    finally:
        if doc is not None and not doc.is_closed:
            doc.close()

    print(f"Images saved in: {output_folder}")
    return output_folder
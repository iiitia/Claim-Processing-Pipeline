import pytesseract
from pdf2image import convert_from_path

def extract_pages(file_path):
    images = convert_from_path(file_path)  # ← removed poppler_path

    pages = []

    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        pages.append({"page_num": i+1, "text": text})

    return pages
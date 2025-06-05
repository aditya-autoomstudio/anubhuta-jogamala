import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageEnhance

# Optional: Advanced preprocessing with OpenCV
# import cv2
# import numpy as np

def preprocess_image_basic(image):
    # Convert to grayscale
    image = image.convert('L')
    # Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    return image

# Advanced preprocessing with OpenCV (optional)
# def preprocess_image_advanced(pil_image):
#     open_cv_image = np.array(pil_image)
#     if open_cv_image.ndim == 3:
#         open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
#     # Binarization
#     _, thresh = cv2.threshold(open_cv_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     # Denoising
#     denoised = cv2.fastNlMeansDenoising(thresh, None, 30, 7, 21)
#     # Convert back to PIL
#     return Image.fromarray(denoised)

pdf_file = 'Anubhuta Jogamala 2 - Ghara Baida.pdf'
out_dir = 'part_2_text'
os.makedirs(out_dir, exist_ok=True)

custom_config = r'--oem 3 --psm 3'
languages = 'ori+eng+hin'

try:
    from pdfplumber import open as pdfplumber_open
    with pdfplumber_open(pdf_file) as pdf:
        for page in pdf.pages:
            page_num = page.page_number
            page_text = page.extract_text()
            if not page_text:
                images = convert_from_path(pdf_file, first_page=page_num, last_page=page_num)
                page_text = ''
                for image in images:
                    # Basic preprocessing
                    pre_image = preprocess_image_basic(image)
                    # For advanced preprocessing, uncomment below:
                    # pre_image = preprocess_image_advanced(image)
                    ocr_text = pytesseract.image_to_string(pre_image, lang=languages, config=custom_config)
                    page_text += ocr_text + '\n'
            txt_path = os.path.join(out_dir, f'page_{page_num:03d}.txt')
            with open(txt_path, 'w', encoding='utf-8') as out:
                out.write(page_text or '')
except Exception as e:
    images = convert_from_path(pdf_file)
    for i, image in enumerate(images, 1):
        pre_image = preprocess_image_basic(image)
        # For advanced preprocessing, uncomment below:
        # pre_image = preprocess_image_advanced(image)
        ocr_text = pytesseract.image_to_string(pre_image, lang=languages, config=custom_config)
        txt_path = os.path.join(out_dir, f'page_{i:03d}.txt')
        with open(txt_path, 'w', encoding='utf-8') as out:
            out.write(ocr_text) 
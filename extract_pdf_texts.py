import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

src = 'Part_1'
dst = 'part_1_text'
os.makedirs(dst, exist_ok=True)

files = [f for f in os.listdir(src) if f.lower().endswith('.pdf')]
for f in sorted(files):
    pdf_path = os.path.join(src, f)
    txt_path = os.path.join(dst, f.rsplit('.', 1)[0] + '.txt')
    text = ''
    try:
        from pdfplumber import open as pdfplumber_open
        with pdfplumber_open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
                else:
                    # Fallback to OCR for this page using Odia
                    images = convert_from_path(pdf_path, first_page=page.page_number, last_page=page.page_number)
                    for image in images:
                        ocr_text = pytesseract.image_to_string(image, lang='ori')
                        text += ocr_text + '\n'
    except Exception as e:
        # If pdfplumber fails, fallback to OCR for all pages using Odia
        images = convert_from_path(pdf_path)
        for image in images:
            ocr_text = pytesseract.image_to_string(image, lang='ori')
            text += ocr_text + '\n'
    with open(txt_path, 'w', encoding='utf-8') as out:
        out.write(text) 
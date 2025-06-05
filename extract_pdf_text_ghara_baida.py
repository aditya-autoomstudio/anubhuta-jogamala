import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

pdf_file = 'Anubhuta Jogamala 2 - Ghara Baida.pdf'
output_file = 'Anubhuta Jogamala 2 - Ghara Baida.txt'

text = ''
try:
    from pdfplumber import open as pdfplumber_open
    with pdfplumber_open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
            else:
                images = convert_from_path(pdf_file, first_page=page.page_number, last_page=page.page_number)
                for image in images:
                    ocr_text = pytesseract.image_to_string(image, lang='ori')
                    text += ocr_text + '\n'
except Exception as e:
    images = convert_from_path(pdf_file)
    for image in images:
        ocr_text = pytesseract.image_to_string(image, lang='ori')
        text += ocr_text + '\n'
with open(output_file, 'w', encoding='utf-8') as out:
    out.write(text) 
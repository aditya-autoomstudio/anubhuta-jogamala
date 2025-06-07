# Anubhuta Jogamala PDF Text Extraction

A Python project for extracting text from "Anubhuta Jogamala" PDF documents with OCR support for Odia language content.

## Project Overview

This project provides comprehensive PDF text extraction capabilities specifically designed for processing Odia language documents from the Anubhuta Jogamala series. It combines direct PDF text extraction with advanced OCR fallback for image-based content.

## Features

- **Multi-language OCR Support**: Odia, English, and Hindi text recognition
- **Advanced Image Preprocessing**: Contrast enhancement and grayscale conversion
- **Fallback Processing**: Automatic OCR when direct text extraction fails
- **Batch Processing**: Handle multiple PDF files simultaneously
- **Page-by-page Extraction**: Individual page processing with detailed logging
- **Type Safety**: Full type hints and mypy compatibility
- **Error Handling**: Comprehensive error handling and logging
- **Modular Design**: Reusable PDFExtractor library

## Project Structure

```
anubhuta-jogamala/
├── pdf_extractor.py              # Main PDF extraction library
├── extract_pdf_texts.py          # Part 1 batch extraction script
├── extract_pdf_texts_part2.py    # Part 2 page-by-page extraction
├── extract_pdf_text_ghara_baida.py # Simple Ghara Baida extraction
├── requirements.txt              # Project dependencies
├── mypy.ini                     # Type checking configuration
├── .gitignore                   # Git ignore rules
├── .cursorrules                 # Cursor AI rules
├── part_1_text/                 # Extracted text from Part 1
├── part_2_text/                 # Extracted text from Part 2
└── README.md                    # This file
```

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR** with Odia language support
3. **poppler-utils** (for pdf2image)

### Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Tesseract (Ubuntu/Debian)
sudo apt-get install tesseract-ocr tesseract-ocr-ori tesseract-ocr-eng tesseract-ocr-hin

# Install poppler-utils (Ubuntu/Debian)
sudo apt-get install poppler-utils

# For Windows, download and install:
# - Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
# - Poppler: https://poppler.freedesktop.org/
```

## Usage

### Using the PDFExtractor Library

```python
from pdf_extractor import create_extractor_with_defaults, PDFExtractionError

# Create extractor with default Odia settings
extractor = create_extractor_with_defaults()

try:
    # Extract text from entire PDF
    text = extractor.extract_text_from_pdf("document.pdf")
    
    # Extract specific page range
    text = extractor.extract_text_from_pdf("document.pdf", page_range=(1, 10))
    
    # Extract pages to individual files
    results = extractor.extract_pages_to_files(
        pdf_path="document.pdf",
        output_dir="output_text",
        file_prefix="page"
    )
    
except PDFExtractionError as e:
    print(f"Extraction failed: {e}")
```

### Running the Scripts

#### Extract Part 1 Texts (Batch Processing)
```bash
python extract_pdf_texts.py
```
- Processes all PDFs in `Part_1/` directory
- Outputs to `part_1_text/` directory

#### Extract Part 2 Pages (Page-by-page)
```bash
python extract_pdf_texts_part2.py
```
- Processes `Anubhuta Jogamala 2 - Ghara Baida.pdf`
- Creates individual page files in `part_2_text/`
- Also creates a complete text file

#### Extract Ghara Baida (Simple)
```bash
python extract_pdf_text_ghara_baida.py
```
- Extracts complete text from Ghara Baida PDF
- Outputs to single text file

## Configuration

### Custom Language Configuration

```python
from pdf_extractor import PDFExtractor

# Custom language and OCR settings
extractor = PDFExtractor(
    languages='ori+eng+hin+san',  # Add Sanskrit
    tesseract_config='--oem 3 --psm 6',  # Different page segmentation
    enable_preprocessing=True
)
```

### Logging Configuration

The project uses Python's built-in logging. To adjust log levels:

```python
import logging
logging.getLogger('pdf_extractor').setLevel(logging.DEBUG)
```

## Error Handling

The project implements comprehensive error handling:

- **PDFExtractionError**: Custom exception for extraction-related errors
- **File Validation**: Checks for file existence and permissions
- **OCR Fallback**: Automatic fallback when direct extraction fails
- **Graceful Degradation**: Continue processing other files if one fails

## Development

### Type Checking

Run mypy for type checking:
```bash
mypy pdf_extractor.py extract_pdf_texts.py
```

### Code Style

The project follows PEP 8 with 88-character line limit (Black default):
- Use f-strings for formatting
- Meaningful variable names
- Comprehensive docstrings
- Type hints for all functions

### Adding New Features

1. Extend the `PDFExtractor` class for new functionality
2. Add appropriate type hints and docstrings
3. Include error handling and logging
4. Update tests and documentation

## Troubleshooting

### Common Issues

1. **Tesseract not found**
   - Ensure Tesseract is installed and in PATH
   - Install Odia language pack

2. **Poor OCR accuracy**
   - Check image quality
   - Adjust preprocessing parameters
   - Try different PSM modes

3. **Memory issues with large PDFs**
   - Process in smaller page ranges
   - Use page-by-page extraction

4. **Encoding issues**
   - Ensure UTF-8 encoding for output files
   - Check locale settings

### Performance Tips

- Use `page_range` parameter for large PDFs
- Enable preprocessing for better OCR accuracy
- Consider caching results for repeated operations
- Process files in batches to manage memory

## License

This project is designed for educational and research purposes related to Odia language document processing.

## Contributing

1. Follow the established code style and cursor rules
2. Add type hints and docstrings
3. Include appropriate error handling
4. Test with various PDF formats
5. Update documentation

## Support

For issues related to:
- **OCR accuracy**: Adjust Tesseract configuration
- **Performance**: Consider page range processing
- **File formats**: Test with different PDF types
- **Dependencies**: Check installation requirements 
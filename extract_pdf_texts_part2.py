"""
Extract text from Anubhuta Jogamala Part 2 (Ghara Baida) PDF file.

This script processes the Part 2 PDF file page by page and extracts text
using advanced OCR with image preprocessing for better accuracy.
"""

import logging
from pathlib import Path
from typing import Dict, Optional

from pdf_extractor import PDFExtractor, PDFExtractionError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract_part2_pages(
    pdf_file: str = 'Anubhuta Jogamala 2 - Ghara Baida.pdf',
    output_dir: str = 'part_2_text',
    page_range: Optional[tuple] = None
) -> Dict[int, str]:
    """
    Extract text from Part 2 PDF file page by page.
    
    Args:
        pdf_file: Path to the PDF file to process
        output_dir: Directory to save individual page text files
        page_range: Optional tuple (start_page, end_page) for range extraction
        
    Returns:
        Dictionary mapping page numbers to output file paths
        
    Raises:
        PDFExtractionError: If extraction process fails
    """
    pdf_path = Path(pdf_file)
    output_path = Path(output_dir)
    
    # Validate input file
    if not pdf_path.exists():
        raise PDFExtractionError(f"PDF file not found: {pdf_path}")
    
    # Create output directory
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created output directory: {output_path}")
    except Exception as e:
        raise PDFExtractionError(f"Cannot create output directory: {e}")
    
    # Initialize PDF extractor with advanced OCR settings
    extractor = PDFExtractor(
        languages='ori+eng+hin',
        tesseract_config='--oem 3 --psm 3',
        enable_preprocessing=True
    )
    
    logger.info(f"Starting page-by-page extraction from: {pdf_path.name}")
    
    try:
        # Extract pages to individual files
        results = extractor.extract_pages_to_files(
            pdf_path=pdf_path,
            output_dir=output_path,
            page_range=page_range,
            file_prefix="page"
        )
        
        logger.info(f"Successfully extracted {len(results)} pages")
        return results
        
    except Exception as e:
        raise PDFExtractionError(f"Failed to extract pages: {e}")


def extract_complete_text(
    pdf_file: str = 'Anubhuta Jogamala 2 - Ghara Baida.pdf',
    output_file: str = 'Anubhuta Jogamala 2 - Ghara Baida.txt'
) -> str:
    """
    Extract complete text from Part 2 PDF file into a single file.
    
    Args:
        pdf_file: Path to the PDF file to process
        output_file: Path for the complete text output file
        
    Returns:
        Path to the output file
        
    Raises:
        PDFExtractionError: If extraction process fails
    """
    pdf_path = Path(pdf_file)
    output_path = Path(output_file)
    
    # Validate input file
    if not pdf_path.exists():
        raise PDFExtractionError(f"PDF file not found: {pdf_path}")
    
    # Initialize PDF extractor
    extractor = PDFExtractor(
        languages='ori+eng+hin',
        tesseract_config='--oem 3 --psm 3',
        enable_preprocessing=True
    )
    
    logger.info(f"Extracting complete text from: {pdf_path.name}")
    
    try:
        # Extract complete text
        extracted_text = extractor.extract_text_from_pdf(pdf_path)
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        
        logger.info(f"Complete text saved to: {output_path}")
        return str(output_path)
        
    except Exception as e:
        raise PDFExtractionError(f"Failed to extract complete text: {e}")


def main() -> None:
    """Main function to execute the text extraction process."""
    pdf_file = 'Anubhuta Jogamala 2 - Ghara Baida.pdf'
    
    try:
        # Check if PDF exists
        if not Path(pdf_file).exists():
            print(f"❌ PDF file not found: {pdf_file}")
            return
        
        print(f"🔄 Processing: {pdf_file}")
        
        # Extract page by page
        print("\n1. Extracting pages individually...")
        page_results = extract_part2_pages(pdf_file)
        
        if page_results:
            print(f"✓ Successfully extracted {len(page_results)} pages:")
            sample_pages = list(page_results.items())[:5]  # Show first 5 pages
            for page_num, file_path in sample_pages:
                print(f"  • Page {page_num} → {Path(file_path).name}")
            if len(page_results) > 5:
                print(f"  • ... and {len(page_results) - 5} more pages")
        
        # Extract complete text
        print("\n2. Extracting complete text...")
        complete_file = extract_complete_text(pdf_file)
        print(f"✓ Complete text saved to: {complete_file}")
        
        print(f"\n🎉 Processing completed successfully!")
        
    except PDFExtractionError as e:
        logger.error(f"Extraction failed: {e}")
        print(f"❌ Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main() 
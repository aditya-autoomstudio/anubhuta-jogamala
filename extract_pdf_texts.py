"""
Extract text from Anubhuta Jogamala Part 1 PDF files.

This script processes PDF files from the Part_1 directory and extracts text
using the PDFExtractor library with OCR fallback for Odia language support.
"""

import logging
from pathlib import Path
from typing import List, Optional

from pdf_extractor import create_extractor_with_defaults, PDFExtractionError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract_part1_texts(
    source_dir: str = 'Part_1',
    output_dir: str = 'part_1_text',
    pdf_pattern: str = '*.pdf'
) -> dict:
    """
    Extract text from all PDF files in the source directory.
    
    Args:
        source_dir: Directory containing PDF files
        output_dir: Directory to save extracted text files
        pdf_pattern: Glob pattern for PDF files
        
    Returns:
        Dictionary mapping PDF filenames to output text files
        
    Raises:
        PDFExtractionError: If extraction process fails
    """
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    # Validate source directory
    if not source_path.exists():
        raise PDFExtractionError(f"Source directory not found: {source_path}")
    
    # Create output directory
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created output directory: {output_path}")
    except Exception as e:
        raise PDFExtractionError(f"Cannot create output directory: {e}")
    
    # Initialize PDF extractor
    extractor = create_extractor_with_defaults()
    
    # Find PDF files
    pdf_files = list(source_path.glob(pdf_pattern))
    if not pdf_files:
        logger.warning(f"No PDF files found in {source_path}")
        return {}
    
    logger.info(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF file
    results = {}
    for pdf_file in sorted(pdf_files):
        try:
            logger.info(f"Processing: {pdf_file.name}")
            
            # Generate output filename
            output_file = output_path / f"{pdf_file.stem}.txt"
            
            # Extract text using the PDFExtractor
            extracted_text = extractor.extract_text_from_pdf(pdf_file)
            
            # Save extracted text
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            
            results[pdf_file.name] = str(output_file)
            logger.info(f"Successfully processed: {pdf_file.name}")
            
        except Exception as e:
            logger.error(f"Failed to process {pdf_file.name}: {e}")
            # Continue processing other files
            continue
    
    logger.info(f"Processing completed. Successfully processed {len(results)} files")
    return results


def main() -> None:
    """Main function to execute the text extraction process."""
    try:
        results = extract_part1_texts()
        
        if results:
            print(f"\n✓ Successfully extracted text from {len(results)} PDF files:")
            for pdf_name, output_file in results.items():
                print(f"  • {pdf_name} → {output_file}")
        else:
            print("⚠ No PDF files were processed.")
            
    except PDFExtractionError as e:
        logger.error(f"Extraction failed: {e}")
        print(f"❌ Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main() 
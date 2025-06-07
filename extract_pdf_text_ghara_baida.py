"""
Extract text from Anubhuta Jogamala 2 - Ghara Baida PDF file.

This is a simple script to extract all text from the Ghara Baida PDF
into a single text file using the PDFExtractor library.
"""

import logging
from pathlib import Path
from typing import Optional

from pdf_extractor import create_extractor_with_defaults, PDFExtractionError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract_ghara_baida_text(
    pdf_file: str = 'Anubhuta Jogamala 2 - Ghara Baida.pdf',
    output_file: str = 'Anubhuta Jogamala 2 - Ghara Baida.txt'
) -> Optional[str]:
    """
    Extract complete text from the Ghara Baida PDF file.
    
    Args:
        pdf_file: Path to the source PDF file
        output_file: Path for the output text file
        
    Returns:
        Path to the output file if successful, None otherwise
        
    Raises:
        PDFExtractionError: If extraction process fails
    """
    pdf_path = Path(pdf_file)
    output_path = Path(output_file)
    
    # Validate input file
    if not pdf_path.exists():
        raise PDFExtractionError(f"PDF file not found: {pdf_path}")
    
    logger.info(f"Starting text extraction from: {pdf_path.name}")
    
    try:
        # Initialize PDF extractor with default Odia settings
        extractor = create_extractor_with_defaults()
        
        # Extract text from the entire PDF
        extracted_text = extractor.extract_text_from_pdf(pdf_path)
        
        if not extracted_text.strip():
            logger.warning("No text was extracted from the PDF")
            return None
        
        # Save extracted text to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        
        logger.info(f"Text extraction completed. Output saved to: {output_path}")
        logger.info(f"Total characters extracted: {len(extracted_text)}")
        
        return str(output_path)
        
    except Exception as e:
        raise PDFExtractionError(f"Failed to extract text: {e}")


def main() -> None:
    """Main function to execute the text extraction process."""
    pdf_file = 'Anubhuta Jogamala 2 - Ghara Baida.pdf'
    output_file = 'Anubhuta Jogamala 2 - Ghara Baida.txt'
    
    try:
        print(f"🔄 Extracting text from: {pdf_file}")
        
        result_file = extract_ghara_baida_text(pdf_file, output_file)
        
        if result_file:
            print(f"✓ Text extraction completed successfully!")
            print(f"📄 Output saved to: {result_file}")
            
            # Display file size
            output_path = Path(result_file)
            if output_path.exists():
                size_kb = output_path.stat().st_size / 1024
                print(f"📊 File size: {size_kb:.1f} KB")
        else:
            print("⚠ No text could be extracted from the PDF")
            
    except PDFExtractionError as e:
        logger.error(f"Extraction failed: {e}")
        print(f"❌ Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main() 